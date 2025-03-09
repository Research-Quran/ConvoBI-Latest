import axios from "axios";

// FastAPI Base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

// Axios instance for FastAPI requests
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Fetch current database name
export const getCurrentDatabase = async (): Promise<string | null> => {
  try {
    const response = await apiClient.get("/current_database/");
    return response.data;
  } catch (error) {
    console.error("Error fetching current database:", error);
    return null;
  }
};

// Upload and process an Excel file
export const uploadFile = async (file: File, fileOption: string = "Replace"): Promise<any> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_option", fileOption);

  try {
    const response = await apiClient.post("/process_file/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error processing file:", error);
    throw error;
  }
};

// Download Metadata Template
export const downloadTemplate = async (): Promise<void> => {
  try {
    const response = await apiClient.get("/download_template/", { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "Metadata_Template.xlsx");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("Error downloading template:", error);
    throw error;
  }
};
