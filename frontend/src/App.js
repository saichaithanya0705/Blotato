import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import { AuthProvider } from "./contexts/AuthContext";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Features from "./pages/Features";
import FAQ from "./pages/FAQ";
import Affiliates from "./pages/Affiliates";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ApiDocs from "./pages/ApiDocs";

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="features" element={<Features />} />
              <Route path="faq" element={<FAQ />} />
              <Route path="affiliates" element={<Affiliates />} />
              <Route path="login" element={<Login />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="api-docs" element={<ApiDocs />} />
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster />
      </AuthProvider>
    </div>
  );
}

export default App;