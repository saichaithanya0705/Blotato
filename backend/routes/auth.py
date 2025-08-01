from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models import (UserCreate, UserLogin, User, AuthResponse, UserResponse,
                   APIKeyCreate, APIKey, APIKeyResponse, APIKeyListItem)
from auth import get_password_hash, verify_password, create_access_token, verify_token, verify_auth, generate_api_key
from storage import users_collection, api_keys_collection
from config import get_config, get_user_data, setup_initial_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/status")
async def get_system_status():
    """Get system configuration status."""
    config = get_config()
    return {
        "configured": config.is_configured(),
        "message": "System ready" if config.is_configured() else "System needs initial setup"
    }

@router.post("/setup", response_model=AuthResponse)
async def setup_system(user_data: UserCreate):
    """Setup the system with initial user (only works if not already configured)."""

    config = get_config()

    # Check if system is already configured
    if config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System is already configured"
        )

    # Setup the initial user
    success = setup_initial_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to setup system"
        )

    # Create access token
    access_token = create_access_token(data={"sub": config.get_user_id()})

    # Get user data
    user_data_dict = get_user_data()
    user_response = UserResponse(
        id=user_data_dict["_id"],
        name=user_data_dict["name"],
        email=user_data_dict["email"],
        avatar=user_data_dict["avatar"],
        plan=user_data_dict["plan"],
        created_at=datetime.fromisoformat(user_data_dict["created_at"])
    )

    return AuthResponse(
        success=True,
        user=user_response,
        token=access_token
    )

@router.post("/login", response_model=AuthResponse)
async def login(login_data: UserLogin):
    """Authenticate user and return token."""

    config = get_config()

    # Check if system is configured
    if not config.is_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System not configured. Please set up the user account first."
        )

    # Validate credentials against single user
    if not config.validate_user_credentials(login_data.email, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create access token
    access_token = create_access_token(data={"sub": config.get_user_id()})

    # Get user data
    user_data = get_user_data()
    user_response = UserResponse(
        id=user_data["_id"],
        name=user_data["name"],
        email=user_data["email"],
        avatar=user_data["avatar"],
        plan=user_data["plan"],
        created_at=datetime.fromisoformat(user_data["created_at"])
    )

    return AuthResponse(
        success=True,
        user=user_response,
        token=access_token
    )

@router.post("/logout")
async def logout(user_id: str = Depends(verify_token)):
    """Logout user (client-side token removal)."""
    return {"success": True, "message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(verify_auth)):
    """Get current user information."""

    user_data = get_user_data()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user_data["_id"],
        name=user_data["name"],
        email=user_data["email"],
        avatar=user_data["avatar"],
        plan=user_data["plan"],
        created_at=datetime.fromisoformat(user_data["created_at"])
    )

# API Key Management Endpoints

@router.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(api_key_data: APIKeyCreate, user_id: str = Depends(verify_token)):
    """Create a new API key for external integrations."""

    # Check if user has reached the maximum number of API keys
    existing_keys = await api_keys_collection.find({"is_active": True})
    config = get_config()

    if len(existing_keys) >= config.max_api_keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum number of API keys ({config.max_api_keys}) reached"
        )

    # Generate new API key
    api_key = generate_api_key()

    # Create API key document
    api_key_doc = {
        "_id": str(uuid.uuid4()),
        "name": api_key_data.name,
        "description": api_key_data.description,
        "key": api_key,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_used": None
    }

    # Save to storage
    result = await api_keys_collection.insert_one(api_key_doc)
    if not result.get("inserted_id"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key"
        )

    return APIKeyResponse(**api_key_doc)

@router.get("/api-keys", response_model=List[APIKeyListItem])
async def list_api_keys(user_id: str = Depends(verify_token)):
    """List all API keys (without showing the full key)."""

    api_keys = await api_keys_collection.find({"is_active": True})

    return [
        APIKeyListItem(
            id=key["_id"],
            name=key["name"],
            description=key.get("description"),
            key_preview=key["key"][:8] + "...",
            is_active=key["is_active"],
            created_at=key["created_at"],
            last_used=key.get("last_used")
        )
        for key in api_keys
    ]

@router.delete("/api-keys/{key_id}")
async def revoke_api_key(key_id: str, user_id: str = Depends(verify_token)):
    """Revoke (deactivate) an API key."""

    result = await api_keys_collection.update_one(
        {"_id": key_id},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )

    if result.get("modified_count", 0) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )

    return {"success": True, "message": "API key revoked successfully"}