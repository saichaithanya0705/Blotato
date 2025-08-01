import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import asyncio
from threading import Lock

class FileStorage:
    """File-based storage system to replace MongoDB."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self._locks = {}
        
        # Initialize data files
        self.files = {
            "user": self.data_dir / "user.json",
            "content": self.data_dir / "content.json", 
            "testimonials": self.data_dir / "testimonials.json",
            "features": self.data_dir / "features.json",
            "faqs": self.data_dir / "faqs.json",
            "api_keys": self.data_dir / "api_keys.json"
        }
        
        # Initialize empty files if they don't exist
        for file_path in self.files.values():
            if not file_path.exists():
                self._write_file(file_path, [])
    
    def _get_lock(self, file_path: Path) -> Lock:
        """Get or create a lock for a specific file."""
        if file_path not in self._locks:
            self._locks[file_path] = Lock()
        return self._locks[file_path]
    
    def _read_file(self, file_path: Path) -> List[Dict]:
        """Read data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_file(self, file_path: Path, data: List[Dict]):
        """Write data to a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    
    async def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        """Find a single document matching the query."""
        file_path = self.files[collection]
        lock = self._get_lock(file_path)
        
        with lock:
            data = self._read_file(file_path)
            
            for item in data:
                if self._matches_query(item, query):
                    return item
            return None
    
    async def find(self, collection: str, query: Dict = None, sort: List[tuple] = None, limit: int = None) -> List[Dict]:
        """Find multiple documents matching the query."""
        file_path = self.files[collection]
        lock = self._get_lock(file_path)
        
        with lock:
            data = self._read_file(file_path)
            
            # Filter by query
            if query:
                data = [item for item in data if self._matches_query(item, query)]
            
            # Sort
            if sort:
                for field, direction in reversed(sort):
                    reverse = direction == -1
                    data.sort(key=lambda x: x.get(field, ''), reverse=reverse)
            
            # Limit
            if limit:
                data = data[:limit]
                
            return data
    
    async def insert_one(self, collection: str, document: Dict) -> Dict:
        """Insert a single document."""
        file_path = self.files[collection]
        lock = self._get_lock(file_path)
        
        with lock:
            data = self._read_file(file_path)
            
            # Add timestamp if not present
            if 'created_at' not in document:
                document['created_at'] = datetime.utcnow()
            if 'updated_at' not in document:
                document['updated_at'] = datetime.utcnow()
                
            data.append(document)
            self._write_file(file_path, data)
            
            return {"inserted_id": document.get("_id")}
    
    async def update_one(self, collection: str, query: Dict, update: Dict) -> Dict:
        """Update a single document."""
        file_path = self.files[collection]
        lock = self._get_lock(file_path)
        
        with lock:
            data = self._read_file(file_path)
            
            for i, item in enumerate(data):
                if self._matches_query(item, query):
                    # Handle $set operator
                    if "$set" in update:
                        item.update(update["$set"])
                    else:
                        item.update(update)
                    
                    item['updated_at'] = datetime.utcnow()
                    data[i] = item
                    self._write_file(file_path, data)
                    return {"modified_count": 1}
            
            return {"modified_count": 0}
    
    async def delete_one(self, collection: str, query: Dict) -> Dict:
        """Delete a single document."""
        file_path = self.files[collection]
        lock = self._get_lock(file_path)
        
        with lock:
            data = self._read_file(file_path)
            
            for i, item in enumerate(data):
                if self._matches_query(item, query):
                    del data[i]
                    self._write_file(file_path, data)
                    return {"deleted_count": 1}
            
            return {"deleted_count": 0}
    
    def _matches_query(self, item: Dict, query: Dict) -> bool:
        """Check if an item matches the query."""
        for key, value in query.items():
            if key not in item or item[key] != value:
                return False
        return True

# Global storage instance
storage = FileStorage()

# Collection interfaces to maintain compatibility
class Collection:
    def __init__(self, name: str):
        self.name = name

    async def find_one(self, query: Dict) -> Optional[Dict]:
        return await storage.find_one(self.name, query)

    async def find(self, query: Dict = None) -> List[Dict]:
        return await storage.find(self.name, query or {})

    async def insert_one(self, document: Dict) -> Dict:
        return await storage.insert_one(self.name, document)

    async def update_one(self, query: Dict, update: Dict) -> Dict:
        return await storage.update_one(self.name, query, update)

    async def delete_one(self, query: Dict) -> Dict:
        return await storage.delete_one(self.name, query)

    def sort(self, field: str, direction: int = 1):
        """Return a cursor-like object for sorting."""
        return SortedCursor(self.name, [(field, direction)])

    def find_cursor(self, query: Dict = None):
        """Return a cursor-like object for querying."""
        return QueryCursor(self.name, query or {})

class QueryCursor:
    def __init__(self, collection_name: str, query: Dict = None):
        self.collection_name = collection_name
        self.query = query or {}
        self.sort_params = None
        self.limit_value = None

    def sort(self, field: str, direction: int = 1):
        """Add sorting to the cursor."""
        self.sort_params = [(field, direction)]
        return self

    def limit(self, limit: int):
        """Add limit to the cursor."""
        self.limit_value = limit
        return self

    async def to_list(self, limit: int = None) -> List[Dict]:
        final_limit = limit or self.limit_value
        return await storage.find(self.collection_name, query=self.query, sort=self.sort_params, limit=final_limit)

class SortedCursor:
    def __init__(self, collection_name: str, sort_params: List[tuple], query: Dict = None):
        self.collection_name = collection_name
        self.sort_params = sort_params
        self.query = query or {}

    async def to_list(self, limit: int = None) -> List[Dict]:
        return await storage.find(self.collection_name, query=self.query, sort=self.sort_params, limit=limit)

# Initialize collections
users_collection = Collection("user")
content_collection = Collection("content")
testimonials_collection = Collection("testimonials")
features_collection = Collection("features")
faqs_collection = Collection("faqs")
api_keys_collection = Collection("api_keys")

async def init_storage():
    """Initialize storage with default data."""
    # Initialize with sample data if files are empty
    await _init_testimonials()
    await _init_features()
    await _init_faqs()

async def _init_testimonials():
    """Initialize testimonials with sample data."""
    existing = await testimonials_collection.find({})
    if not existing:
        sample_testimonials = [
            {
                "_id": "testimonial-1",
                "name": "Sarah Johnson",
                "title": "Content Creator",
                "avatar": "https://ui-avatars.com/api/?name=Sarah+Johnson&background=6366f1&color=fff",
                "rating": 5,
                "content": "This platform has revolutionized my content creation workflow. I can manage all my social media posts from one place!",
                "has_video": False,
                "is_active": True,
                "created_at": "2024-01-01T00:00:00"
            },
            {
                "_id": "testimonial-2",
                "name": "Mike Chen",
                "title": "Digital Marketer",
                "avatar": "https://ui-avatars.com/api/?name=Mike+Chen&background=6366f1&color=fff",
                "rating": 5,
                "content": "The analytics features help me track engagement across all platforms. Highly recommended!",
                "has_video": False,
                "is_active": True,
                "created_at": "2024-01-02T00:00:00"
            }
        ]

        for testimonial in sample_testimonials:
            await testimonials_collection.insert_one(testimonial)

async def _init_features():
    """Initialize features with sample data."""
    existing = await features_collection.find({})
    if not existing:
        sample_features = [
            {
                "_id": "feature-1",
                "title": "Multi-Platform Publishing",
                "description": "Publish your content across multiple social media platforms simultaneously",
                "icon": "share-2",
                "is_active": True,
                "order": 1
            },
            {
                "_id": "feature-2",
                "title": "Analytics Dashboard",
                "description": "Track engagement, views, and performance metrics in real-time",
                "icon": "bar-chart-3",
                "is_active": True,
                "order": 2
            },
            {
                "_id": "feature-3",
                "title": "Content Scheduling",
                "description": "Schedule your posts for optimal engagement times",
                "icon": "calendar",
                "is_active": True,
                "order": 3
            }
        ]

        for feature in sample_features:
            await features_collection.insert_one(feature)

async def _init_faqs():
    """Initialize FAQs with sample data."""
    existing = await faqs_collection.find({})
    if not existing:
        sample_faqs = [
            {
                "_id": "faq-1",
                "question": "How do I connect my social media accounts?",
                "answer": "You can connect your accounts through the dashboard settings. We support all major platforms including Twitter, Instagram, LinkedIn, and Facebook.",
                "is_active": True,
                "order": 1
            },
            {
                "_id": "faq-2",
                "question": "Can I schedule posts in advance?",
                "answer": "Yes! You can schedule posts up to 6 months in advance. Our system will automatically publish them at your specified times.",
                "is_active": True,
                "order": 2
            },
            {
                "_id": "faq-3",
                "question": "Is there an API for developers?",
                "answer": "Absolutely! We provide a comprehensive REST API that allows you to integrate our platform with your existing tools and workflows.",
                "is_active": True,
                "order": 3
            }
        ]

        for faq in sample_faqs:
            await faqs_collection.insert_one(faq)
