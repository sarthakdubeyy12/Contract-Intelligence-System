import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Contract from "./pages/Contract";
import Scoring from "./pages/Scoring";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import React from "react";

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/contracts" element={<Contract />} />
            <Route path="/scoring" element={<Scoring />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;