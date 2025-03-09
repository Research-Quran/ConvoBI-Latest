"use client";
import { useEffect, useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import axios from "axios"; // ✅ Using Axios for API calls


const Lineage = () => {
  const [currentDB, setCurrentDB] = useState("");
  const [model, setModel] = useState("");
  const [promptData, setPromptData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userPrompt, setUserPrompt] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const [dbResponse, modelResponse, promptResponse] = await Promise.all([
          axios.get("http://localhost:8000/current_database/"),
          axios.get("http://localhost:8000/config/"),
          axios.get("http://localhost:8000/prompt/", {
            params: { input_text: "your_query_here" },
          }),
        ]);

        setCurrentDB(dbResponse.data.current_db || "N/A");
        setModel(modelResponse.data.model || "N/A");
        setPromptData(promptResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Current Database: {currentDB}</h1>
      <h2 className="text-lg font-semibold">Model: {model}</h2>

      {loading ? (
        <p className="mt-4">Loading...</p>
      ) : (
        <div className="mt-4">
          <p className="font-semibold">
            <span className="text-blue-600">Prompt:</span> {promptData?.Prompt || "N/A"}
          </p>

          {promptData?.Response?.lineage ? (
            <div className="mt-6">
              {promptData.Response.lineage.map((item, index) => (
                <div key={index} className="mb-6">
                  <h3 className="text-lg font-bold">{item.description}</h3>
                  <div className="overflow-x-auto mt-2">
                    <table className="w-full border-collapse border bg-white shadow-md">
                      <thead className="bg-gray-200">
                        <tr>
                          {Object.keys(item.data[0] || {}).map((key) => (
                            <th key={key} className="border px-4 py-2 text-left">{key}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {item.data.map((row, rowIndex) => (
                          <tr key={rowIndex} className="hover:bg-gray-100">
                            {Object.values(row).map((value, colIndex) => (
                              <td key={colIndex} className="border px-4 py-2">{value}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No table data available.</p>
          )}

          {/* Input Box for User Prompt */}
          <div className="mt-6 flex items-center">
            <input
              type="text"
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              placeholder="Enter your prompt"
              className="w-full border border-gray-300 px-4 py-2 rounded-md shadow-sm"
            />
            <button className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              ➤
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const LineagePage = () => {
  return (
    <DefaultLayout>
      <Lineage />
    </DefaultLayout>
  );
};

export default LineagePage;
