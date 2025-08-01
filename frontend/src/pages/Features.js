import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Brain, Video, RefreshCw, Share2, Calendar, BarChart3 } from "lucide-react";
import { publicAPI } from "../services/api";
import { mockData } from "../utils/mockData";

const Features = () => {
  const [features, setFeatures] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        const response = await publicAPI.getFeatures();
        setFeatures(response.data);
      } catch (error) {
        console.error("Failed to fetch features:", error);
        // Fallback to mock data
        setFeatures(mockData.features);
      } finally {
        setLoading(false);
      }
    };

    fetchFeatures();
  }, []);

  const getIcon = (iconName) => {
    const icons = {
      brain: Brain,
      video: Video,
      refresh: RefreshCw,
      share: Share2,
      calendar: Calendar,
      chart: BarChart3
    };
    const IconComponent = icons[iconName] || Brain;
    return <IconComponent className="w-8 h-8" />;
  };

  return (
    <div className="min-h-screen bg-slate-950 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-slate-800 text-purple-300 border-purple-500/30">
            Features
          </Badge>
          <h1 className="text-4xl sm:text-6xl font-bold mb-6">
            Everything you need to{" "}
            <span className="bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              scale your content
            </span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            From AI-powered creation to multi-platform distribution, Blotato provides all the tools you need to build a successful social media presence.
          </p>
        </div>

        {/* Features Grid */}
        {loading ? (
          <div className="text-center text-gray-400">Loading features...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={feature.id || index} className="bg-slate-900 border-slate-700 hover:bg-slate-800 transition-all duration-300 hover:scale-105">
                <CardHeader>
                  <div className="flex items-center mb-4">
                    <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-3 rounded-lg">
                      {getIcon(feature.icon)}
                    </div>
                  </div>
                  <CardTitle className="text-white text-xl">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Call to Action */}
        <div className="text-center mt-20">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to transform your content strategy?
          </h2>
          <p className="text-gray-300 mb-8 text-lg max-w-2xl mx-auto">
            Join thousands of creators who are scaling their social media presence with Blotato's AI-powered platform.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transform hover:scale-105 transition-all duration-200">
              Start Creating Now
            </button>
            <button className="bg-slate-800 hover:bg-slate-700 text-white px-8 py-4 rounded-xl font-semibold text-lg border border-slate-600 transition-colors">
              Watch Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Features;