// src/pages/Home.jsx
import { Link } from "react-router-dom";
import React from "react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen text-center">
      <h1 className="text-4xl font-bold mb-6">📄 Contract Intelligence</h1>
      <p className="text-lg mb-8">Upload, Parse, and Score Contracts with ease.</p>

      <Link
        to="/contracts"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
      >
        Get Started
      </Link>
    </div>
  );
}