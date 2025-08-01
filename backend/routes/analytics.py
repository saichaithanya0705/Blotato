from fastapi import APIRouter, Depends
from typing import List
from models import UserStats, RecentContentItem
from auth import verify_auth
from storage import content_collection
import random

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/stats", response_model=UserStats)
async def get_user_stats(user_id: str = Depends(verify_auth)):
    """Get analytics stats for the authenticated user."""

    # Get all content for the user
    content_list = await content_collection.find({"user_id": user_id})

    # Calculate counts
    total_content = len(content_list)
    posts_count = len([c for c in content_list if c.get("type") == "post"])
    videos_count = len([c for c in content_list if c.get("type") == "video"])

    # Calculate engagement
    total_engagement = sum([
        content.get("engagement", {}).get("views", 0) +
        content.get("engagement", {}).get("likes", 0) +
        content.get("engagement", {}).get("shares", 0)
        for content in content_list
    ])

    # Mock followers growth based on content activity
    followers_growth = min(total_content * 50 + random.randint(100, 500), 5000)

    return UserStats(
        posts_created=posts_count,
        videos_generated=videos_count,
        total_engagement=total_engagement,
        followers_growth=followers_growth
    )

@router.get("/recent-content", response_model=List[RecentContentItem])
async def get_recent_content(user_id: str = Depends(verify_auth)):
    """Get recent content for the authenticated user."""

    cursor = content_collection.find_cursor({"user_id": user_id}).sort("created_at", -1).limit(5)
    content_list = await cursor.to_list()
    
    recent_items = []
    for content in content_list:
        engagement_text = "Not published"
        if content.get("status") == "published":
            views = content.get("engagement", {}).get("views", 0)
            likes = content.get("engagement", {}).get("likes", 0)
            if views > 0:
                engagement_text = f"{views:,} views"
            elif likes > 0:
                engagement_text = f"{likes:,} likes"
        elif content.get("status") == "scheduled":
            engagement_text = "Scheduled"
        
        recent_items.append(RecentContentItem(
            id=content["_id"],
            type=content["type"].title(),
            title=content["title"],
            platform=content["platform"],
            status=content["status"].title(),
            engagement=engagement_text
        ))
    
    return recent_items