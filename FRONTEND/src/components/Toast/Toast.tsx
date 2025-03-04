import React, { JSX } from "react";

type ToastType = "success" | "error" | "warning" | "info";

interface ToastProps {
  id: number;
  message: string;
  type: ToastType;
  onClose: (id: number) => void;
}

const Toast: React.FC<ToastProps> = ({ id, message, type, onClose }) => {
  const toastStyles: Record<ToastType, string> = {
    success: "bg-green-500 text-white", 
    error: "bg-red-500 text-white", 
    warning: "text-orange-500 bg-orange-100 dark:bg-orange-700 dark:text-orange-200",
    info: "text-blue-500 bg-blue-100 dark:bg-blue-800 dark:text-blue-200",
  };

  const icons: Record<ToastType, JSX.Element> = {
    success: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />
      </svg>
    ),
    error: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z" />
      </svg>
    ),
    warning: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z" />
      </svg>
    ),
    info: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 2a8 8 0 1 0 8 8A8 8 0 0 0 10 2ZM9 7a1 1 0 1 1 2 0v4a1 1 0 1 1-2 0Zm1 8a1.1 1.1 0 1 1 0-2 1.1 1.1 0 0 1 0 2Z" />
      </svg>
    ),
  };

  return (
    <div className="fixed top-18 right-4 z-50">
      <div className={`flex items-center w-full max-w-xs p-4 text-sm font-medium rounded-lg shadow-lg ${toastStyles[type]}`}>
        <div className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-opacity-20">
          {icons[type]}
          <span className="sr-only">{type} icon</span>
        </div>
        <div className="ml-3">{message}</div>
        <button
          type="button"
          className="ml-auto hover:text-gray-300"
          onClick={() => onClose(id)}
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Toast;
