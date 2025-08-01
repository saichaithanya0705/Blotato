import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const Layout = () => {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;