from fastapi import APIRouter
from typing import List
from models import Testimonial, Feature, FAQ
from storage import testimonials_collection, features_collection, faqs_collection

router = APIRouter(prefix="/public", tags=["Public Data"])

@router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    """Get all active testimonials."""

    cursor = testimonials_collection.find_cursor({"is_active": True}).sort("created_at", -1)
    testimonials = await cursor.to_list(1000)

    return [Testimonial(**testimonial) for testimonial in testimonials]

@router.get("/features", response_model=List[Feature])
async def get_features():
    """Get all active features."""

    cursor = features_collection.find_cursor({"is_active": True}).sort("order", 1)
    features = await cursor.to_list(1000)

    return [Feature(**feature) for feature in features]

@router.get("/faqs", response_model=List[FAQ])
async def get_faqs():
    """Get all active FAQs."""

    cursor = faqs_collection.find_cursor({"is_active": True}).sort("order", 1)
    faqs = await cursor.to_list(1000)

    return [FAQ(**faq) for faq in faqs]