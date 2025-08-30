// src/components/ResultView.jsx
import { useEffect, useState } from "react";
import api from "../api/api";
import React from "react";

export default function ResultView({ contractId }) {
  const [contract, setContract] = useState(null);

  useEffect(() => {
    if (!contractId) return;

    const fetchContract = async () => {
      try {
        const res = await api.get(`/contracts/${contractId}`);
        setContract(res.data);
      } catch (err) {
        console.error("Error fetching contract:", err);
      }
    };

    fetchContract();
  }, [contractId]);

  if (!contract) return null;

  return (
    <div className="p-4 bg-green-50 rounded-lg shadow-md mt-4">
      <h3 className="text-lg font-semibold mb-2">Contract Details</h3>
      <p><strong>ID:</strong> {contract.id}</p>
      <p><strong>Name:</strong> {contract.name}</p>
      <p><strong>Status:</strong> {contract.status}</p>

      <a
        href={`http://localhost:8000/api/v1/contracts/${contract.id}/download`}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-block bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
      >
        Download
      </a>
    </div>
  );
}