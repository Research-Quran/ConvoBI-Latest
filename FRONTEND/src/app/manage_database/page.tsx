"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import DefaultLayout from "@/components/Layouts/DefaultLayout";

const ManageDatabases = () => {
  const [currentDb, setCurrentDb] = useState("");
  const [databases, setDatabases] = useState([]);
  const [selectedDb, setSelectedDb] = useState(""); // Track selected DB for button color

  // Fetch Current Database
  useEffect(() => {
    axios
      .get("http://localhost:8000/current_database/")
      .then((response) => setCurrentDb(response.data.current_db))
      .catch((error) =>
        console.error("Error fetching current database:", error)
      );
  }, []);

  // Fetch List of Databases
  useEffect(() => {
    axios
      .get("http://localhost:8000/databases/")
      .then((response) => setDatabases(response.data.databases))
      .catch((error) => console.error("Error fetching databases:", error));
  }, []);

  // Handle Database Selection
  const handleSelect = (dbName) => {
    axios
      .post("http://localhost:8000/select_database/", { db_name: dbName })
      .then((response) => {
        console.log(response.data);
        setCurrentDb(dbName);
        setSelectedDb(dbName); // Highlight selected button

        // Reset button color after 2-3 seconds
        setTimeout(() => setSelectedDb(""), 500);
      })
      .catch((error) => console.error("Error selecting database:", error));
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-2xl">
        {/* Current Database */}
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          Current Database: <span className="text-blue-600">{currentDb}</span>
        </h2>

        {/* Table for Databases */}
        <h3 className="text-lg font-medium text-gray-600 mb-2">
          List of all databases
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-200 text-gray-700">
                <th className="border px-4 py-2">Sl No</th>
                <th className="border px-4 py-2">Table</th>
                <th className="border px-4 py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {databases.map((db, index) => (
                <tr key={index} className="border-b">
                  <td className="border px-4 py-2 text-green-600 font-semibold">
                    {index + 1}
                  </td>
                  <td className="border px-4 py-2 text-gray-700">{db}</td>
                  <td className="border px-4 py-2">
                    <button
                      className={`px-3 py-1 rounded-md transition ${
                        selectedDb === db
                          ? "bg-green-500 text-white"
                          : "bg-white text-gray-700 border border-gray-400 hover:bg-gray-100"
                      }`}
                      onClick={() => handleSelect(db)}
                    >
                      Select
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const ManageDatabasesPage = () => {
  return (
    <DefaultLayout>
      <ManageDatabases />
    </DefaultLayout>
  );
};

// ✅ Export only **one** default component
export default ManageDatabasesPage;
