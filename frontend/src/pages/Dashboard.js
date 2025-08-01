import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import {
  BarChart3,
  Video,
  FileText,
  Calendar,
  TrendingUp,
  Users,
  Plus,
  Settings,
  Key,
  Code
} from "lucide-react";
import { analyticsAPI } from "../services/api";
import ApiKeyManager from "../components/ApiKeyManager";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    posts_created: 0,
    videos_generated: 0,
    total_engagement: 0,
    followers_growth: 0
  });
  const [recentContent, setRecentContent] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsResponse, contentResponse] = await Promise.all([
          analyticsAPI.getUserStats(),
          analyticsAPI.getRecentContent()
        ]);
        
        setStats(statsResponse.data);
        setRecentContent(contentResponse.data);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const statCards = [
    {
      title: "Posts Created",
      value: stats.posts_created.toString(),
      change: "+12%",
      icon: FileText
    },
    {
      title: "Videos Generated",
      value: stats.videos_generated.toString(),
      change: "+8%",
      icon: Video
    },
    {
      title: "Total Engagement",
      value: stats.total_engagement > 1000 ? `${(stats.total_engagement / 1000).toFixed(1)}K` : stats.total_engagement.toString(),
      change: "+23%",
      icon: TrendingUp
    },
    {
      title: "Followers Growth",
      value: stats.followers_growth > 1000 ? `${(stats.followers_growth / 1000).toFixed(1)}K` : stats.followers_growth.toString(),
      change: "+15%",
      icon: Users
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 py-8 flex items-center justify-center">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-gray-400">
            Here's what's happening with your content today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => {
            const IconComponent = stat.icon;
            return (
              <Card key={index} className="bg-slate-900 border-slate-700">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-2 rounded-lg">
                      <IconComponent className="w-5 h-5 text-white" />
                    </div>
                    <Badge 
                      className={`${
                        stat.change.startsWith('+') 
                          ? 'bg-green-900 text-green-300' 
                          : 'bg-red-900 text-red-300'
                      }`}
                    >
                      {stat.change}
                    </Badge>
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-1">
                    {stat.value}
                  </h3>
                  <p className="text-gray-400 text-sm">
                    {stat.title}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Content Management */}
          <div className="lg:col-span-2">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-white">Recent Content</CardTitle>
                  <Button 
                    size="sm"
                    className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Create New
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {recentContent.length === 0 ? (
                  <div className="text-center py-8 text-gray-400">
                    <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No content created yet.</p>
                    <p className="text-sm">Start creating your first piece of content!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {recentContent.map((content, index) => (
                      <div key={content.id || index} className="flex items-center justify-between p-4 bg-slate-800 rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-2 rounded">
                            {content.type === 'Video' ? (
                              <Video className="w-4 h-4 text-white" />
                            ) : (
                              <FileText className="w-4 h-4 text-white" />
                            )}
                          </div>
                          <div>
                            <h4 className="text-white font-medium">{content.title}</h4>
                            <p className="text-gray-400 text-sm">{content.platform}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge 
                            className={`mb-1 ${
                              content.status === 'Published' 
                                ? 'bg-green-900 text-green-300'
                                : content.status === 'Scheduled'
                                ? 'bg-blue-900 text-blue-300'
                                : 'bg-gray-700 text-gray-300'
                            }`}
                          >
                            {content.status}
                          </Badge>
                          <p className="text-gray-400 text-sm">{content.engagement}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-white"
                  variant="outline"
                >
                  <Video className="w-4 h-4 mr-2" />
                  Create Faceless Video
                </Button>
                <Button 
                  className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-white"
                  variant="outline"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Generate Viral Post
                </Button>
                <Button 
                  className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-white"
                  variant="outline"
                >
                  <Calendar className="w-4 h-4 mr-2" />
                  Schedule Content
                </Button>
                <Button
                  className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-white"
                  variant="outline"
                >
                  <BarChart3 className="w-4 h-4 mr-2" />
                  View Analytics
                </Button>
                <Link to="/api-docs">
                  <Button
                    className="w-full justify-start bg-slate-800 hover:bg-slate-700 text-white"
                    variant="outline"
                  >
                    <Code className="w-4 h-4 mr-2" />
                    API Documentation
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* API Key Management */}
            <ApiKeyManager />

            {/* Account Info */}
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Account</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-3 mb-4">
                  <img
                    src={user?.avatar}
                    alt={user?.name}
                    className="w-12 h-12 rounded-full"
                  />
                  <div>
                    <h4 className="text-white font-medium">{user?.name}</h4>
                    <p className="text-gray-400 text-sm">{user?.email}</p>
                  </div>
                </div>
                <Badge className="bg-gradient-to-r from-pink-500 to-purple-600 text-white mb-4">
                  {user?.plan || 'Free'} Plan
                </Badge>
                <Button 
                  variant="outline" 
                  size="sm"
                  className="w-full bg-slate-800 hover:bg-slate-700 text-white border-slate-600"
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Account Settings
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;