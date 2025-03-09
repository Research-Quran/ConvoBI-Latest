


"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import DefaultLayout from "@/components/Layouts/DefaultLayout";

const MetadataImport = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [importMode, setImportMode] = useState("Replace");
  const [currentDatabase, setCurrentDatabase] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState<boolean | null>(null);

  // Fetch Current Database
  useEffect(() => {
    axios
      .get("http://localhost:8000/current_database/")
      .then((response) => setCurrentDatabase(response.data.current_db || "No database found"))
      .catch((error) => console.error("Error fetching database:", error));
  }, []);

  // Handle File Selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  // Handle File Upload & Process
  const handleSubmit = async () => {
    if (!selectedFile) {
      setMessage("Please select a file first.");
      setIsSuccess(false);
      return;
    }

    setLoading(true);
    setProgress(0);
    setMessage(null);

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("file_option", importMode);

    try {
      const response = await axios.post("http://localhost:8000/process_file/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
          setProgress(percentCompleted);
        },
      });

      setMessage(response.data.message);
      setIsSuccess(true);
    } catch (error) {
      setMessage("File upload failed. Please try again.");
      setIsSuccess(false);
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(null), 5000); // Hide message after 5 seconds
    }
  };

  // Handle Template Download
  const downloadTemplate = () => {
    window.location.href = "http://localhost:8000/download_template/";
  };

  return (
    <div className="flex flex-col p-6 bg-white shadow-md rounded-lg w-[50%] mx-auto">
      {/* Database Info */}
      <h2 className="text-2xl font-semibold text-gray-800">Metadata Import</h2>
      <p className="mt-2 text-gray-600">
        <strong>Current Database:</strong> {currentDatabase || "Loading..."}
      </p>

      {/* Download Template Button */}
      <button
        onClick={downloadTemplate}
        className="mt-4 border border-gray-300 px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition"
      >
        Download Template for Metadata
      </button>

      {/* Import Mode Selection */}
      <div className="mt-6">
        <p className="text-gray-700 font-medium">Action on File Import:</p>
        <div className="flex items-center gap-6 mt-2">
          <label className="flex items-center gap-2 text-gray-700">
            <input
              type="radio"
              value="Append"
              checked={importMode === "Append"}
              onChange={() => setImportMode("Append")}
              className="w-4 h-4 text-blue-600 focus:ring-blue-500"
            />
            Append
          </label>
          <label className="flex items-center gap-2 text-gray-700">
            <input
              type="radio"
              value="Replace"
              checked={importMode === "Replace"}
              onChange={() => setImportMode("Replace")}
              className="w-4 h-4 text-red-600 focus:ring-red-500"
            />
            Replace
          </label>
        </div>
      </div>

      {/* File Upload Section */}
      <div className="mt-6 border-dashed border-2 border-gray-300 rounded-lg p-6 text-center">
        <input type="file" accept=".xlsx" id="fileUpload" onChange={handleFileChange} className="hidden" />
        <label htmlFor="fileUpload" className="cursor-pointer flex flex-col items-center justify-center">
          <span className="text-gray-500">Drag and drop file here or</span>
          <span className="mt-2 bg-gray-200 px-4 py-2 rounded-lg hover:bg-gray-300 transition">
            Browse files
          </span>
        </label>
        {selectedFile && <p className="mt-2 text-green-600">{selectedFile.name}</p>}
        <p className="text-sm text-gray-500 mt-2">Limit 200MB per file • XLSX</p>
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        className={`mt-6 px-6 py-2 rounded-lg transition ${
          loading ? "bg-gray-400 cursor-not-allowed" : "bg-green-500 text-white hover:bg-green-600"
        }`}
      >
        {loading ? `Uploading... ${progress}%` : "Upload & Process"}
      </button>

      {/* Progress Bar */}
      {loading && (
        <div className="mt-4 w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-green-500 h-4 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}

      {/* Success / Error Message */}
      {message && (
        <div
          className={`mt-4 p-3 rounded-lg text-center ${
            isSuccess ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
          }`}
        >
          {message}
        </div>
      )}
    </div>
  );
};

const MetadataImportPage = () => {
  return (
    <DefaultLayout>
      <MetadataImport />
    </DefaultLayout>
  );
};

export default MetadataImportPage;
