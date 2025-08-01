# Blotato Clone - Backend Integration Contracts

## API Contracts

### Authentication Endpoints
```
POST /api/auth/signup
Body: { name: string, email: string, password: string }
Response: { success: boolean, user: UserObject, token: string }

POST /api/auth/login  
Body: { email: string, password: string }
Response: { success: boolean, user: UserObject, token: string }

POST /api/auth/logout
Headers: { Authorization: Bearer <token> }
Response: { success: boolean }

GET /api/auth/me
Headers: { Authorization: Bearer <token> }
Response: { user: UserObject }
```

### Content Management Endpoints
```
GET /api/content
Headers: { Authorization: Bearer <token> }
Response: { content: ContentObject[] }

POST /api/content
Headers: { Authorization: Bearer <token> }
Body: { title: string, type: string, platform: string, content: string }
Response: { success: boolean, content: ContentObject }

PUT /api/content/:id
Headers: { Authorization: Bearer <token> }
Body: { title?: string, status?: string, content?: string }
Response: { success: boolean, content: ContentObject }

DELETE /api/content/:id
Headers: { Authorization: Bearer <token> }
Response: { success: boolean }
```

### Analytics Endpoints
```
GET /api/analytics/stats
Headers: { Authorization: Bearer <token> }
Response: { stats: StatsObject }

GET /api/analytics/recent-content
Headers: { Authorization: Bearer <token> }
Response: { content: ContentObject[] }
```

### Public Endpoints
```
GET /api/testimonials
Response: { testimonials: TestimonialObject[] }

GET /api/features
Response: { features: FeatureObject[] }

GET /api/faqs
Response: { faqs: FAQObject[] }
```

## Data Models

### User
```typescript
{
  _id: ObjectId,
  name: string,
  email: string,
  password: string (hashed),
  avatar?: string,
  plan: 'free' | 'pro' | 'premium',
  createdAt: Date,
  updatedAt: Date
}
```

### Content
```typescript
{
  _id: ObjectId,
  userId: ObjectId,
  title: string,
  type: 'post' | 'video',
  platform: string,
  content: string,
  status: 'draft' | 'scheduled' | 'published',
  engagement: {
    views?: number,
    likes?: number,
    shares?: number
  },
  createdAt: Date,
  updatedAt: Date
}
```

### Testimonial
```typescript
{
  _id: ObjectId,
  name: string,
  title: string,
  avatar: string,
  rating: number,
  content: string,
  hasVideo: boolean,
  isActive: boolean,
  createdAt: Date
}
```

## Mock Data to Replace

### In `/app/frontend/src/utils/mockData.js`:
- **testimonials**: Replace with real testimonials from database
- **stats**: Replace with real user analytics
- **features**: Replace with dynamic features from database
- **faqs**: Replace with dynamic FAQs from database

### In `/app/frontend/src/contexts/AuthContext.js`:
- **login()**: Replace mock implementation with real API call
- **signup()**: Replace mock implementation with real API call
- **user state**: Load from JWT token verification

### In `/app/frontend/src/pages/Dashboard.js`:
- **stats**: Replace mock stats with real user analytics
- **recentContent**: Replace with real user content from database

## Backend Implementation Plan

### 1. Database Schema
- User authentication with JWT
- Content management system
- Testimonials management
- Analytics tracking

### 2. Authentication System
- JWT-based authentication
- Password hashing with bcrypt
- Protected routes middleware
- User session management

### 3. Content Management
- CRUD operations for user content
- Content categorization by type and platform
- Status tracking (draft, scheduled, published)
- Basic analytics integration

### 4. Public Data Management
- Testimonials CRUD (admin-only)
- Features management
- FAQ management

## Frontend Integration Changes

### Authentication Context Updates
1. Replace localStorage-based auth with JWT token management
2. Add token refresh logic
3. Update login/signup to call real API endpoints
4. Add proper error handling for auth failures

### API Integration
1. Replace mock data calls with axios API calls to backend
2. Add loading states for all API operations
3. Implement proper error handling and user feedback
4. Add JWT token to all authenticated requests

### Dashboard Updates  
1. Fetch real user stats from analytics API
2. Load actual user content from content API
3. Implement real content creation workflow
4. Add proper loading and error states

### Public Pages Updates
1. Load testimonials from database
2. Fetch features dynamically
3. Load FAQs from backend
4. Add admin interface for content management (future enhancement)

## Security Considerations
- Input validation and sanitization
- Rate limiting on auth endpoints
- JWT token expiration and refresh
- CORS properly configured
- Password strength requirements
- XSS and injection protection

## Database Collections
- users
- content
- testimonials
- features
- faqs
- analytics (for future expansion)