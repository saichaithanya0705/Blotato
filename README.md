# Blotato Single User - Self-Hosted Content Management Platform

A single-user, self-hosted content management platform with API access for external integrations. Similar to self-hosted n8n, this provides a personal instance with full API capabilities.

## 🚀 Features

- **Single User System**: No multi-user complexity, just your personal content management platform
- **API-First Design**: Full REST API with authentication for external integrations
- **File-Based Storage**: No database required - all data stored in JSON files
- **API Key Management**: Generate and manage API keys for external applications
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Content Management**: Create, edit, and organize your content across platforms
- **Analytics Dashboard**: Track your content performance and engagement

## 🛠️ Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

3. **Start the Backend**
   ```bash
   python start.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   yarn install
   ```

2. **Configure Backend URL**
   ```bash
   # Create .env file in frontend directory
   echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env
   ```

3. **Start the Frontend**
   ```bash
   yarn start
   ```

   The web interface will be available at `http://localhost:3000`

### Initial Setup

1. Visit `http://localhost:3000`
2. You'll be redirected to the setup page if the system isn't configured
3. Create your admin account
4. Start using your personal Blotato instance!

## 🔑 API Usage

### Authentication

The API supports two authentication methods:

1. **JWT Tokens** (for web interface)
2. **API Keys** (for external integrations)

### Creating API Keys

1. Login to the web interface
2. Go to Dashboard
3. Find the "API Keys" section
4. Click "Create API Key"
5. Give it a name and description
6. Copy the generated key (you won't see it again!)

### Using API Keys

Include your API key in the request header:

```bash
curl -H "X-API-Key: your-api-key-here" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/content
```

### API Endpoints

- `GET /api/content` - Get all content
- `POST /api/content` - Create new content
- `PUT /api/content/{id}` - Update content
- `DELETE /api/content/{id}` - Delete content
- `GET /api/analytics/stats` - Get user statistics
- `GET /api/analytics/recent-content` - Get recent content
- `GET /api/public/testimonials` - Get testimonials (no auth required)
- `GET /api/public/features` - Get features (no auth required)
- `GET /api/public/faqs` - Get FAQs (no auth required)

Full API documentation is available at `/api-docs` in the web interface.

## 📁 Configuration

### Environment Variables

**Backend (.env)**:
```bash
# JWT Secret (IMPORTANT: Change in production!)
JWT_SECRET_KEY=your-super-secret-jwt-key

# Data Directory
DATA_DIR=data

# Single User Configuration (Optional - can be set via web interface)
BLOTATO_USER_NAME=Your Name
BLOTATO_USER_EMAIL=your.email@example.com
BLOTATO_USER_PASSWORD=your-secure-password
BLOTATO_USER_PLAN=premium

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Frontend (.env)**:
```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Data Storage

All data is stored in JSON files in the `data/` directory:
- `user.json` - User configuration
- `content.json` - Your content
- `api_keys.json` - API keys
- `testimonials.json` - Testimonials
- `features.json` - Features
- `faqs.json` - FAQs

## 🔒 Security

- **Change the JWT secret** in production
- **Use HTTPS** in production
- **Keep API keys secure** - never expose them in client-side code
- **Regular backups** of the `data/` directory
- **Firewall protection** - only expose necessary ports

## 🚀 Production Deployment

### Using Docker (Recommended)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  blotato-backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - JWT_SECRET_KEY=your-production-secret-key
      - HOST=0.0.0.0
      - PORT=8000

  blotato-frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8000
```

### Manual Deployment

1. Set up a reverse proxy (nginx/Apache)
2. Configure SSL certificates
3. Set production environment variables
4. Start both backend and frontend services
5. Set up process management (systemd/supervisor)

## 🤝 Integration Examples

### Python
```python
import requests

api_key = "your-api-key-here"
base_url = "http://localhost:8000/api"

headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

# Create content
response = requests.post(f"{base_url}/content",
    headers=headers,
    json={
        "title": "My New Post",
        "type": "post",
        "platform": "twitter",
        "content": "Hello from the API!"
    }
)
print(response.json())
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

const apiKey = 'your-api-key-here';
const baseURL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL,
    headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json'
    }
});

// Get all content
api.get('/content')
    .then(response => console.log(response.data))
    .catch(error => console.error(error));
```

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/api-docs`
2. Review the logs in the backend console
3. Ensure all dependencies are installed correctly
4. Verify your API keys are correctly configured

---

**Happy content managing! 🎉**
