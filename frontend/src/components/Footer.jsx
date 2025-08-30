import React from "react";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-400 text-center py-4 mt-10">
      <p>
        © {new Date().getFullYear()} ContractAI. All Rights Reserved.
      </p>
    </footer>
  );
};

export default Footer;