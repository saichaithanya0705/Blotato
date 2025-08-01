import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Code, Key, Database, Zap } from "lucide-react";

const ApiDocs = () => {
  const endpoints = [
    {
      method: "GET",
      path: "/api/content",
      description: "Get all content",
      auth: "Required",
      response: "Array of content objects"
    },
    {
      method: "POST",
      path: "/api/content",
      description: "Create new content",
      auth: "Required",
      body: {
        title: "string",
        type: "post | video",
        platform: "string",
        content: "string"
      },
      response: "Created content object"
    },
    {
      method: "PUT",
      path: "/api/content/{id}",
      description: "Update content",
      auth: "Required",
      body: {
        title: "string (optional)",
        status: "draft | scheduled | published (optional)",
        content: "string (optional)"
      },
      response: "Updated content object"
    },
    {
      method: "DELETE",
      path: "/api/content/{id}",
      description: "Delete content",
      auth: "Required",
      response: "Success message"
    },
    {
      method: "GET",
      path: "/api/analytics/stats",
      description: "Get user statistics",
      auth: "Required",
      response: "Statistics object"
    },
    {
      method: "GET",
      path: "/api/analytics/recent-content",
      description: "Get recent content",
      auth: "Required",
      response: "Array of recent content items"
    },
    {
      method: "GET",
      path: "/api/public/testimonials",
      description: "Get testimonials",
      auth: "None",
      response: "Array of testimonials"
    },
    {
      method: "GET",
      path: "/api/public/features",
      description: "Get features",
      auth: "None",
      response: "Array of features"
    },
    {
      method: "GET",
      path: "/api/public/faqs",
      description: "Get FAQs",
      auth: "None",
      response: "Array of FAQs"
    }
  ];

  const getMethodColor = (method) => {
    switch (method) {
      case "GET": return "bg-green-600";
      case "POST": return "bg-blue-600";
      case "PUT": return "bg-yellow-600";
      case "DELETE": return "bg-red-600";
      default: return "bg-gray-600";
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Code className="w-8 h-8 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">API Documentation</h1>
          </div>
          <p className="text-gray-400 text-lg">
            Integrate your applications with the Blotato API
          </p>
        </div>

        {/* Authentication Section */}
        <Card className="bg-slate-900 border-slate-800 mb-8">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Key className="w-5 h-5 text-purple-400" />
              <CardTitle className="text-white">Authentication</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-gray-300">
              The API uses API key authentication. Include your API key in the request header:
            </p>
            <div className="bg-slate-800 p-4 rounded-lg">
              <code className="text-green-400 font-mono">
                X-API-Key: your-api-key-here
              </code>
            </div>
            <p className="text-gray-400 text-sm">
              You can generate API keys from your dashboard. Keep your API keys secure and never expose them in client-side code.
            </p>
          </CardContent>
        </Card>

        {/* Base URL Section */}
        <Card className="bg-slate-900 border-slate-800 mb-8">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Database className="w-5 h-5 text-purple-400" />
              <CardTitle className="text-white">Base URL</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-800 p-4 rounded-lg">
              <code className="text-blue-400 font-mono">
                {process.env.REACT_APP_BACKEND_URL || "http://localhost:8000"}
              </code>
            </div>
          </CardContent>
        </Card>

        {/* Endpoints Section */}
        <Card className="bg-slate-900 border-slate-800 mb-8">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-purple-400" />
              <CardTitle className="text-white">API Endpoints</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {endpoints.map((endpoint, index) => (
                <div key={index} className="border border-slate-700 rounded-lg p-4">
                  <div className="flex items-center space-x-3 mb-3">
                    <Badge className={`${getMethodColor(endpoint.method)} text-white`}>
                      {endpoint.method}
                    </Badge>
                    <code className="text-blue-400 font-mono">{endpoint.path}</code>
                  </div>
                  
                  <p className="text-gray-300 mb-3">{endpoint.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-white font-medium mb-2">Authentication</h4>
                      <Badge variant={endpoint.auth === "Required" ? "destructive" : "secondary"}>
                        {endpoint.auth}
                      </Badge>
                    </div>
                    
                    {endpoint.body && (
                      <div>
                        <h4 className="text-white font-medium mb-2">Request Body</h4>
                        <div className="bg-slate-800 p-3 rounded text-sm">
                          <pre className="text-gray-300">
                            {JSON.stringify(endpoint.body, null, 2)}
                          </pre>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="mt-4">
                    <h4 className="text-white font-medium mb-2">Response</h4>
                    <p className="text-gray-400 text-sm">{endpoint.response}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Example Section */}
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-white">Example Request</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <h3 className="text-white font-medium">Create Content</h3>
              <div className="bg-slate-800 p-4 rounded-lg">
                <pre className="text-gray-300 text-sm overflow-x-auto">
{`curl -X POST "${process.env.REACT_APP_BACKEND_URL || "http://localhost:8000"}/api/content" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: your-api-key-here" \\
  -d '{
    "title": "My New Post",
    "type": "post",
    "platform": "twitter",
    "content": "This is my new post content!"
  }'`}
                </pre>
              </div>
              
              <h3 className="text-white font-medium">Response</h3>
              <div className="bg-slate-800 p-4 rounded-lg">
                <pre className="text-gray-300 text-sm overflow-x-auto">
{`{
  "id": "content-123",
  "title": "My New Post",
  "type": "post",
  "platform": "twitter",
  "content": "This is my new post content!",
  "status": "draft",
  "engagement": {
    "views": 0,
    "likes": 0,
    "shares": 0
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}`}
                </pre>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ApiDocs;
