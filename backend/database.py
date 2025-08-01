from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db: AsyncIOMotorDatabase = client[os.environ['DB_NAME']]

# Collections
users_collection = db.users
content_collection = db.content
testimonials_collection = db.testimonials
features_collection = db.features
faqs_collection = db.faqs

async def init_db():
    """Initialize database with default data."""
    
    # Create indexes
    await users_collection.create_index("email", unique=True)
    await content_collection.create_index([("user_id", 1), ("created_at", -1)])
    
    # Check if testimonials exist, if not create default ones
    testimonials_count = await testimonials_collection.count_documents({})
    if testimonials_count == 0:
        default_testimonials = [
            {
                "name": "MICHAEL WATSON",
                "title": "Forever Building Wealth", 
                "avatar": "https://ui-avatars.com/api/?name=Michael+Watson&background=1e293b&color=ffffff",
                "rating": 4,
                "content": "Michael Watson from Dallas, TX. First thing first, before Blotato I was using multiple subs just to create content. The best part about Blotato, it's your one stop shop. Everything you need, all in one piece, for an awesome monthly price. If you are considering Blotato and you want to grow your social media, look no...",
                "has_video": False,
                "is_active": True
            },
            {
                "name": "DEVON RODRIGUEZ",
                "title": "Content Creator at Youtube",
                "avatar": "https://ui-avatars.com/api/?name=Devon+Rodriguez&background=1e293b&color=ffffff",
                "rating": 5,
                "content": "Hi, I'm Devon Rodriguez from New York City. Before discovering Bloytato, I was navigating the complexities of starting a faceless YouTube channel, facing trial and error. Since then, Blotato has been a game-changer, allowing me to create videos I'm truly proud of. The platform's ease of use, comprehensive support, and...",
                "has_video": True,
                "is_active": True
            },
            {
                "name": "PETER",
                "title": "Peter E-bike Store Thailand",
                "avatar": "https://ui-avatars.com/api/?name=Peter&background=1e293b&color=ffffff",
                "rating": 5,
                "content": "Hello my name is Peter from Thailand. I mostly use Facebook, Instagram and TikTok to post text, photos and videos to promote my products and services. Before I used the Blotato, I had to spend a lot of time promoting my content myself and it was a waste of time. But...",
                "has_video": True,
                "is_active": True
            },
            {
                "name": "JASON BRYAN",
                "title": "SmartFiBw",
                "avatar": "https://ui-avatars.com/api/?name=Jason+Bryan&background=1e293b&color=ffffff",
                "rating": 5,
                "content": "Hello, My name is Jason Bryan from Baltimore, Maryland. I have a new business and I'm with the thought of consistently posting in order to drive traffic to my business...",
                "has_video": True,
                "is_active": True
            },
            {
                "name": "SARAH CHEN",
                "title": "Digital Marketing Expert",
                "avatar": "https://ui-avatars.com/api/?name=Sarah+Chen&background=1e293b&color=ffffff",
                "rating": 5,
                "content": "Blotato has revolutionized how I create content for my clients. The AI-powered features save me hours every week, and the quality is consistently high. My engagement rates have increased by 300% since using this platform.",
                "has_video": False,
                "is_active": True
            }
        ]
        await testimonials_collection.insert_many(default_testimonials)
    
    # Check if features exist, if not create default ones
    features_count = await features_collection.count_documents({})
    if features_count == 0:
        default_features = [
            {
                "title": "AI-Powered Content Creation",
                "description": "Generate viral posts with our AI trained on 100,000+ successful social media posts",
                "icon": "brain",
                "is_active": True,
                "order": 1
            },
            {
                "title": "Faceless Video Generation", 
                "description": "Create engaging videos with AI voiceovers, animations, and subtitles without showing your face",
                "icon": "video",
                "is_active": True,
                "order": 2
            },
            {
                "title": "Content Remixing",
                "description": "Transform YouTube videos, articles, and other content into multiple social media posts",
                "icon": "refresh",
                "is_active": True,
                "order": 3
            },
            {
                "title": "Multi-Platform Publishing",
                "description": "Post simultaneously to LinkedIn, TikTok, Twitter, Facebook, Instagram, and more",
                "icon": "share",
                "is_active": True,
                "order": 4
            },
            {
                "title": "Content Calendar",
                "description": "Plan and schedule your content with our intuitive calendar system",
                "icon": "calendar",
                "is_active": True,
                "order": 5
            },
            {
                "title": "Analytics Dashboard",
                "description": "Track performance across all platforms with detailed insights and metrics",
                "icon": "chart",
                "is_active": True,
                "order": 6
            }
        ]
        await features_collection.insert_many(default_features)
    
    # Check if FAQs exist, if not create default ones
    faqs_count = await faqs_collection.count_documents({})
    if faqs_count == 0:
        default_faqs = [
            {
                "question": "What is Blotato?",
                "answer": "Blotato is an AI-powered content creation platform that helps you create, remix, and distribute viral social media content across multiple platforms. It's designed for content creators, solopreneurs, and businesses who want to scale their social media presence efficiently.",
                "is_active": True,
                "order": 1
            },
            {
                "question": "How does the AI content generation work?",
                "answer": "Our AI has been trained on over 100,000 viral social media posts to understand what makes content engaging. Simply input your topic or existing content, and our AI will generate multiple variations optimized for different platforms.",
                "is_active": True,
                "order": 2
            },
            {
                "question": "Can I create videos without showing my face?",
                "answer": "Yes! Blotato specializes in faceless video creation. Our platform generates videos with AI voiceovers, animations, and subtitles, perfect for those who prefer to stay behind the camera.",
                "is_active": True,
                "order": 3
            },
            {
                "question": "Which social media platforms are supported?",
                "answer": "Blotato supports all major platforms including LinkedIn, TikTok, Twitter/X, Facebook, Instagram, Threads, and Pinterest. You can post to multiple platforms simultaneously.",
                "is_active": True,
                "order": 4
            },
            {
                "question": "Is there a free trial?",
                "answer": "Yes, you can start with our free trial to explore all features and see how Blotato can transform your content creation process.",
                "is_active": True,
                "order": 5
            },
            {
                "question": "How much content can I create per week?",
                "answer": "With Blotato, you can easily create 50+ pieces of content per week across all your social media platforms, helping you maintain a consistent and engaging presence.",
                "is_active": True,
                "order": 6
            }
        ]
        await faqs_collection.insert_many(default_faqs)