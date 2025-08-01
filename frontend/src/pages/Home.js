import React, { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Star, Play } from "lucide-react";
import { Link } from "react-router-dom";
import { publicAPI } from "../services/api";
import { mockData } from "../utils/mockData";

const Home = () => {
  const [testimonials, setTestimonials] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTestimonials = async () => {
      try {
        const response = await publicAPI.getTestimonials();
        setTestimonials(response.data);
      } catch (error) {
        console.error("Failed to fetch testimonials:", error);
        // Fallback to mock data
        setTestimonials(mockData.testimonials);
      } finally {
        setLoading(false);
      }
    };

    fetchTestimonials();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-20 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-b from-purple-900/20 via-slate-950 to-slate-950" />
        <div className="relative max-w-4xl mx-auto text-center">
          <Badge className="mb-8 bg-slate-800 text-purple-300 border-purple-500/30 hover:bg-slate-700">
            #1 AI Content Engine
          </Badge>
          
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold mb-8 leading-tight">
            Create{" "}
            <span className="bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              viral posts
            </span>{" "}
            and{" "}
            <span className="bg-gradient-to-r from-pink-500 via-orange-500 to-purple-500 bg-clip-text text-transparent">
              faceless videos
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl text-gray-300 mb-4 max-w-3xl mx-auto">
            All-in-one solution to create, remix, and distribute
          </p>
          <p className="text-lg sm:text-xl text-purple-300 font-semibold mb-8">
            50+ pieces of content per week{" "}
            <span className="text-gray-300">to build your brand and faceless channels.</span>
          </p>
          
          <Link to="/signup">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-200"
            >
              Start Creating
            </Button>
          </Link>
        </div>
      </section>

      {/* Style Showcase */}
      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-center space-x-4 mb-16 overflow-x-auto">
            {mockData.contentStyles.map((style, index) => (
              <Badge
                key={index}
                className="whitespace-nowrap bg-slate-800 text-gray-300 border-slate-600 hover:bg-slate-700"
              >
                {style}
              </Badge>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-16">
            Testimonials
          </h2>
          
          {loading ? (
            <div className="text-center text-gray-400">Loading testimonials...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              {testimonials.map((testimonial, index) => (
                <Card key={testimonial.id || index} className="bg-slate-900 border-slate-700 hover:bg-slate-800 transition-colors">
                  <CardContent className="p-6">
                    <div className="flex items-center mb-4">
                      <img
                        src={testimonial.avatar}
                        alt={testimonial.name}
                        className="w-10 h-10 rounded-full mr-3"
                      />
                      <div>
                        <h4 className="text-white font-semibold text-sm">
                          {testimonial.name}
                        </h4>
                        <p className="text-gray-400 text-xs">
                          {testimonial.title}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex mb-3">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                    
                    <p className="text-gray-300 text-sm mb-4 line-clamp-4">
                      {testimonial.content}
                    </p>
                    
                    {testimonial.has_video && (
                      <div className="relative bg-slate-800 rounded-lg p-8 flex items-center justify-center">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="text-white hover:bg-slate-700"
                        >
                          <Play className="w-6 h-6" />
                        </Button>
                      </div>
                    )}
                    
                    <button className="text-purple-400 text-sm hover:text-purple-300 transition-colors">
                      show more
                    </button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Social Proof Stats */}
      <section className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-16">
            Built by the fastest-growing AI influencer
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {mockData.stats.map((stat, index) => (
              <Card key={index} className="bg-slate-900/50 border-slate-700">
                <CardContent className="p-8 text-center">
                  <h3 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent mb-2">
                    {stat.value}
                  </h3>
                  <p className="text-gray-300 text-sm">
                    {stat.label}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
          
          {/* Analytics Preview */}
          <div className="mt-16 max-w-2xl mx-auto">
            <Card className="bg-slate-900 border-slate-700">
              <CardContent className="p-6">
                <div className="bg-gray-200 rounded-lg p-6 mb-4">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-gray-800 font-medium">Analytics Overview</span>
                    <span className="text-gray-600 text-sm">May 2024</span>
                  </div>
                  <div className="h-32 bg-gradient-to-r from-pink-200 to-purple-200 rounded-lg flex items-end justify-center">
                    <div className="text-gray-700 text-sm">📈 Growth Chart</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;