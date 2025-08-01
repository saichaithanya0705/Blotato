import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Button } from "./ui/button";
import { useAuth } from "../contexts/AuthContext";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-slate-950/90 backdrop-blur-sm border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 via-purple-500 to-orange-500 flex items-center justify-center">
              <span className="text-white text-sm font-bold">B</span>
            </div>
            <span className="text-white text-xl font-bold">BLOTATO</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/features"
              className={`text-sm font-medium transition-colors ${
                isActive("/features")
                  ? "text-pink-400"
                  : "text-gray-300 hover:text-white"
              }`}
            >
              Features
            </Link>
            <Link
              to="/faq"
              className={`text-sm font-medium transition-colors ${
                isActive("/faq")
                  ? "text-pink-400"
                  : "text-gray-300 hover:text-white"
              }`}
            >
              FAQ
            </Link>
            <Link
              to="/affiliates"
              className={`text-sm font-medium transition-colors ${
                isActive("/affiliates")
                  ? "text-pink-400"
                  : "text-gray-300 hover:text-white"
              }`}
            >
              Affiliates
            </Link>
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={user.avatar} alt={user.name} />
                      <AvatarFallback>{user.name.charAt(0).toUpperCase()}</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56 bg-slate-900 border-slate-700" align="end">
                  <DropdownMenuItem onClick={() => navigate("/dashboard")} className="text-gray-300 hover:text-white hover:bg-slate-800">
                    Dashboard
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate("/api-docs")} className="text-gray-300 hover:text-white hover:bg-slate-800">
                    API Documentation
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogout} className="text-gray-300 hover:text-white hover:bg-slate-800">
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <>
                <Link to="/login">
                  <Button className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white">
                    Login
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;