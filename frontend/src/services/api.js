import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance
const api = axios.create({
  baseURL: API,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("blotato_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Public API calls
export const publicAPI = {
  getTestimonials: () => api.get("/public/testimonials"),
  getFeatures: () => api.get("/public/features"),
  getFAQs: () => api.get("/public/faqs"),
};

// Content API calls
export const contentAPI = {
  getUserContent: () => api.get("/content"),
  createContent: (data) => api.post("/content", data),
  updateContent: (id, data) => api.put(`/content/${id}`, data),
  deleteContent: (id) => api.delete(`/content/${id}`),
};

// Analytics API calls
export const analyticsAPI = {
  getUserStats: () => api.get("/analytics/stats"),
  getRecentContent: () => api.get("/analytics/recent-content"),
};

export default api;