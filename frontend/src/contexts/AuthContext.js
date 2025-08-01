import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("blotato_token"));

  // Set up axios interceptor for auth token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check for stored user data and validate token
  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem("blotato_token");
      if (storedToken) {
        try {
          const response = await axios.get(`${API}/auth/me`);
          setUser(response.data);
          setToken(storedToken);
        } catch (error) {
          // Token is invalid, clear stored data
          localStorage.removeItem("blotato_token");
          localStorage.removeItem("blotato_user");
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password
      });

      const { user: userData, token: authToken } = response.data;
      
      setUser(userData);
      setToken(authToken);
      localStorage.setItem("blotato_token", authToken);
      localStorage.setItem("blotato_user", JSON.stringify(userData));
      
      return { success: true };
    } catch (error) {
      console.error("Login error:", error);
      const message = error.response?.data?.detail || "Login failed";
      throw new Error(message);
    }
  };

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get(`${API}/auth/status`);
      return response.data;
    } catch (error) {
      console.error("Status check error:", error);
      return { configured: false, message: "Unable to check system status" };
    }
  };

  const setupSystem = async (email, password, name) => {
    try {
      const response = await axios.post(`${API}/auth/setup`, {
        name,
        email,
        password
      });

      const { user: userData, token: authToken } = response.data;

      setUser(userData);
      setToken(authToken);
      localStorage.setItem("blotato_token", authToken);
      localStorage.setItem("blotato_user", JSON.stringify(userData));

      return { success: true };
    } catch (error) {
      console.error("Setup error:", error);
      const message = error.response?.data?.detail || "System setup failed";
      throw new Error(message);
    }
  };

  const logout = async () => {
    try {
      await axios.post(`${API}/auth/logout`);
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem("blotato_token");
      localStorage.removeItem("blotato_user");
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const value = {
    user,
    login,
    setupSystem,
    checkSystemStatus,
    logout,
    loading,
    token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};