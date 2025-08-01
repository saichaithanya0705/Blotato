from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

# Enums
class PlanType(str, Enum):
    free = "free"
    pro = "pro"
    premium = "premium"

class ContentType(str, Enum):
    post = "post"
    video = "video"

class ContentStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    published = "published"

# Base Models
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('ObjectId required')
        return str(v)

# User Models
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    avatar: Optional[str] = None
    plan: PlanType = PlanType.free
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    avatar: Optional[str] = None
    plan: PlanType
    created_at: datetime

# Auth Models
class AuthResponse(BaseModel):
    success: bool
    user: UserResponse
    token: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Content Models
class ContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    type: ContentType
    platform: str
    content: str

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ContentStatus] = None
    content: Optional[str] = None

class Engagement(BaseModel):
    views: Optional[int] = 0
    likes: Optional[int] = 0
    shares: Optional[int] = 0

class Content(ContentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    status: ContentStatus = ContentStatus.draft
    engagement: Engagement = Field(default_factory=Engagement)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Testimonial Models
class TestimonialBase(BaseModel):
    name: str
    title: str
    avatar: str
    rating: int = Field(..., ge=1, le=5)
    content: str
    has_video: bool = False

class TestimonialCreate(TestimonialBase):
    pass

class Testimonial(TestimonialBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Feature Models
class FeatureBase(BaseModel):
    title: str
    description: str
    icon: str

class Feature(FeatureBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    is_active: bool = True
    order: int = 0
    
    class Config:
        populate_by_name = True

# FAQ Models
class FAQBase(BaseModel):
    question: str
    answer: str

class FAQ(FAQBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    is_active: bool = True
    order: int = 0
    
    class Config:
        populate_by_name = True

# Analytics Models
class UserStats(BaseModel):
    posts_created: int = 0
    videos_generated: int = 0
    total_engagement: int = 0
    followers_growth: int = 0

class RecentContentItem(BaseModel):
    id: str
    type: str
    title: str
    platform: str
    status: str
    engagement: str

# API Key Models
class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class APIKey(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    description: Optional[str] = None
    key: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class APIKeyResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    key: str  # Only shown once during creation
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime] = None

class APIKeyListItem(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    key_preview: str  # Only first 8 characters + "..."
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime] = None