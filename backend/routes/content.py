from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models import ContentCreate, ContentUpdate, Content
from auth import verify_auth
from storage import content_collection
import uuid
from datetime import datetime

router = APIRouter(prefix="/content", tags=["Content Management"])

@router.get("/", response_model=List[Content])
async def get_user_content(user_id: str = Depends(verify_auth)):
    """Get all content for the authenticated user."""

    cursor = content_collection.find_cursor({"user_id": user_id}).sort("created_at", -1)
    content_list = await cursor.to_list(1000)

    return [Content(**content) for content in content_list]

@router.post("/", response_model=Content)
async def create_content(content_data: ContentCreate, user_id: str = Depends(verify_auth)):
    """Create new content for the authenticated user."""
    
    content_dict = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "title": content_data.title,
        "type": content_data.type,
        "platform": content_data.platform,
        "content": content_data.content,
        "status": "draft",
        "engagement": {
            "views": 0,
            "likes": 0,
            "shares": 0
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await content_collection.insert_one(content_dict)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create content"
        )
    
    return Content(**content_dict)

@router.put("/{content_id}", response_model=Content)
async def update_content(
    content_id: str,
    update_data: ContentUpdate,
    user_id: str = Depends(verify_auth)
):
    """Update content for the authenticated user."""

    # Check if content exists and belongs to user
    existing_content = await content_collection.find_one({
        "_id": content_id,
        "user_id": user_id
    })

    if not existing_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Prepare update data
    update_dict = {"updated_at": datetime.utcnow()}
    if update_data.title is not None:
        update_dict["title"] = update_data.title
    if update_data.status is not None:
        update_dict["status"] = update_data.status
    if update_data.content is not None:
        update_dict["content"] = update_data.content

    # Update content
    await content_collection.update_one(
        {"_id": content_id, "user_id": user_id},
        {"$set": update_dict}
    )

    # Get updated content
    updated_content = await content_collection.find_one({
        "_id": content_id,
        "user_id": user_id
    })

    return Content(**updated_content)

@router.delete("/{content_id}")
async def delete_content(content_id: str, user_id: str = Depends(verify_auth)):
    """Delete content for the authenticated user."""

    result = await content_collection.delete_one({
        "_id": content_id,
        "user_id": user_id
    })

    if result.get("deleted_count", 0) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return {"success": True, "message": "Content deleted successfully"}