"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";

const LogViewer = () => {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/logs/stream");

    eventSource.onmessage = (event) => {
      setLogs((prevLogs) => [...prevLogs, event.data]);
    };

    eventSource.onerror = () => {
      console.error("EventSource failed.");
      eventSource.close();
    };

    return () => eventSource.close();
  }, []);

  return (
    <div className="mt-6 p-6 bg-white shadow-md rounded-lg w-[60%] mx-auto">
      <h2 className="text-xl font-semibold text-gray-800">Real-time Logs</h2>
      <div className="mt-4 p-4 bg-gray-100 rounded-lg h-60 overflow-y-auto border border-gray-300">
        {logs.map((log, index) => (
          <p key={index} className="text-sm text-gray-700">{log}</p>
        ))}
      </div>
    </div>
  );
};

export default LogViewer;
