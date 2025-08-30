// src/pages/Contract.jsx
import { useState } from "react";
import UploadForm from "../components/UploadForm";
import StatusCard from "../components/StatusCard";
import ResultView from "../components/ResultView";
import React from "react";

export default function Contract() {
  const [taskId, setTaskId] = useState(null);
  const [contractId, setContractId] = useState(null);

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Contract Upload & Processing</h1>

      {!taskId && !contractId && (
        <UploadForm onUploadSuccess={(id) => setTaskId(id)} />
      )}

      {taskId && !contractId && (
        <StatusCard taskId={taskId} onComplete={(id) => setContractId(id)} />
      )}

      {contractId && <ResultView contractId={contractId} />}
    </div>
  );
}