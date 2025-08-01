import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { DollarSign, Users, TrendingUp, Award } from "lucide-react";

const Affiliates = () => {
  const benefits = [
    {
      icon: <DollarSign className="w-8 h-8" />,
      title: "High Commissions",
      description: "Earn up to 30% recurring commission for every successful referral"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Growing Market",
      description: "Content creation is exploding - join a market that's growing rapidly"
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Marketing Support",
      description: "Get access to banners, landing pages, and marketing materials"
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: "Premium Support",
      description: "Dedicated affiliate manager and priority support for your success"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-slate-800 text-purple-300 border-purple-500/30">
            Affiliate Program
          </Badge>
          <h1 className="text-4xl sm:text-6xl font-bold mb-6">
            Earn money promoting{" "}
            <span className="bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 bg-clip-text text-transparent">
              Blotato
            </span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Join our affiliate program and earn generous commissions while helping content creators scale their social media presence.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <Card className="bg-slate-900 border-slate-700 text-center">
            <CardContent className="p-8">
              <h3 className="text-4xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent mb-2">
                30%
              </h3>
              <p className="text-gray-300">Commission Rate</p>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700 text-center">
            <CardContent className="p-8">
              <h3 className="text-4xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent mb-2">
                90 days
              </h3>
              <p className="text-gray-300">Cookie Duration</p>
            </CardContent>
          </Card>
          <Card className="bg-slate-900 border-slate-700 text-center">
            <CardContent className="p-8">
              <h3 className="text-4xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent mb-2">
                $2,500
              </h3>
              <p className="text-gray-300">Average Monthly Earning</p>
            </CardContent>
          </Card>
        </div>

        {/* Benefits */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            Why join our affiliate program?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <Card key={index} className="bg-slate-900 border-slate-700 hover:bg-slate-800 transition-colors">
                <CardHeader>
                  <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-3 rounded-lg w-fit">
                    {benefit.icon}
                  </div>
                  <CardTitle className="text-white text-xl">
                    {benefit.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    {benefit.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* How it works */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            How it works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>                <div className="bg-gradient-to-r from-pink-500 to-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-4">
                  1
                </div>
                <CardTitle className="text-white">
                  Apply & Get Approved
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Fill out our simple application form and get approved within 24 hours.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <div className="bg-gradient-to-r from-pink-500 to-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-4">
                  2
                </div>
                <CardTitle className="text-white">
                  Share Your Link
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Get your unique affiliate link and start promoting Blotato to your audience.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-slate-900 border-slate-700">
              <CardHeader>
                <div className="bg-gradient-to-r from-pink-500 to-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-4">
                  3
                </div>
                <CardTitle className="text-white">
                  Earn Commission
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  Earn 30% recurring commission for every successful referral you make.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <Card className="bg-gradient-to-r from-slate-900 to-slate-800 border-slate-700 p-12">
            <CardContent>
              <h2 className="text-3xl font-bold text-white mb-6">
                Ready to start earning?
              </h2>
              <p className="text-gray-300 mb-8 text-lg max-w-2xl mx-auto">
                Join our affiliate program today and start earning generous commissions while helping creators succeed.
              </p>
              <Button 
                size="lg"
                className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-200"
              >
                Apply Now
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Affiliates;