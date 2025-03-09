"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import DefaultLayout from "@/components/Layouts/DefaultLayout";

const DatabaseInfo = () => {
  const [currentDatabase, setCurrentDatabase] = useState("Loading...");
  const [databaseInfo, setDatabaseInfo] = useState([]);

  // Fetch current database name
  useEffect(() => {
    axios
      .get("http://localhost:8000/current_database/")
      .then((response) => {
        setCurrentDatabase(response.data.current_db);
      })
      .catch((error) => {
        console.error("Error fetching current database:", error);
      });
  }, []);

  // Fetch database info
  useEffect(() => {
    axios
      .get("http://localhost:8000/database_info/")
      .then((response) => {
        setDatabaseInfo(response.data.database_info);
      })
      .catch((error) => {
        console.error("Error fetching database info:", error);
      });
  }, []);

  return (
    <DefaultLayout>
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-5xl">
          {/* Current Database */}
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Current Database: <span className="text-blue-600">{currentDatabase}</span>
          </h2>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-200 text-gray-700">
                  <th className="border px-4 py-2">Schema</th>
                  <th className="border px-4 py-2">Table</th>
                  <th className="border px-4 py-2">No Of Columns</th>
                  <th className="border px-4 py-2">Size</th>
                </tr>
              </thead>
              <tbody>
                {databaseInfo.map((db, index) => (
                  <tr key={index} className="border-b">
                    <td className="border px-4 py-2">{db.Schema}</td>
                    <td className="border px-4 py-2 font-semibold text-gray-700">
                      {db.Table}
                    </td>
                    <td className="border px-4 py-2 text-center">{db["No Of Columns"]}</td>
                    <td className="border px-4 py-2">{db.Size}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default DatabaseInfo;
