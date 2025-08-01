#!/usr/bin/env python3
"""
Blotato Single User - Startup Script
"""

import uvicorn
import os
from pathlib import Path

def main():
    """Start the Blotato API server."""

    # Set default environment variables if not set
    # Railway provides PORT automatically
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", os.environ.get("PORT", "8000"))
    os.environ.setdefault("DATA_DIR", "data")
    
    # Create data directory if it doesn't exist
    data_dir = Path(os.environ.get("DATA_DIR", "data"))
    data_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting Blotato Single User API...")
    print(f"📁 Data directory: {data_dir.absolute()}")
    print(f"🌐 Server will be available at: http://{os.environ['HOST']}:{os.environ['PORT']}")
    print("📖 API documentation will be available at: /docs")
    print()
    
    # Check if system is configured
    from config import get_config
    config = get_config()
    
    if config.is_configured():
        print("✅ System is configured and ready!")
        print(f"👤 User: {config.user_config.name} ({config.user_config.email})")
    else:
        print("⚠️  System not configured yet.")
        print("🔧 Visit the web interface to complete initial setup.")
    
    print()
    print("🔑 To create API keys for external integrations:")
    print("   1. Complete the initial setup (if not done)")
    print("   2. Login to the web interface")
    print("   3. Go to Dashboard > API Keys section")
    print()
    
    # Start the server
    uvicorn.run(
        "server:app",
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
