// src/components/StatusCard.jsx
import { useEffect, useState } from "react";
import api from "../api/api";
import React from "react";

export default function StatusCard({ taskId, onComplete }) {
  const [status, setStatus] = useState("pending");

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/contracts/status/${taskId}`);
        setStatus(res.data.status);

        if (res.data.status === "completed") {
          clearInterval(interval);
          onComplete(res.data.contract_id);
        }
      } catch (err) {
        console.error(err);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [taskId, onComplete]);

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md mt-4 text-center">
      <h3 className="text-lg font-medium">Processing Status</h3>
      <p className="mt-2">
        {status === "pending" ? "Processing..." : `Status: ${status}`}
      </p>
    </div>
  );
}