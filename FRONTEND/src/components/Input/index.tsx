import React, { useState } from "react";
import { cn } from "@/lib/utils"; // Utility function for conditional classNames
import ValidationMessage, { ValidationMessageType } from "../ValidationMessage";

interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size"> {
  label?: string;
  variant?: "default" | "outline" | "error" | "success";
  size?: "sm" | "md" | "lg";
  search?: boolean; // New prop to show search icon
  validationMessage?: string;
  messageType?: ValidationMessageType;
}

const Input: React.FC<InputProps> = ({
  label,
  id,
  variant = "default",
  size = "md",
  className,
  required = false,
  messageType,
  search = false, // Default false
  validationMessage,
  ...props
}) => {
  const baseStyles =
    "h-11 w-full rounded-lg border appearance-none px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-none focus:ring dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 bg-transparent text-gray-800 border-gray-300 focus:border-brand-300 focus:ring-brand-500/20 dark:border-gray-700 dark:text-white/90 dark:focus:border-brand-800";

  const variantStyles = {
    default: "border-gray-300 bg-white text-gray-900 focus:ring-blue-400",
    outline:
      "border border-gray-400 bg-transparent text-gray-700 focus:ring-gray-500",
    error: "border-red-500 bg-red-100 text-red-900 focus:ring-red-400",
    success:
      "border-green-500 bg-green-100 text-green-900 focus:ring-green-400",
  };

  const sizeStyles = {
    sm: "px-3 py-1 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-5 py-3 text-lg",
  };

  return (
    <div className="flex flex-col space-y-1">
      {label ? (
        <label htmlFor={id} className="text-sm font-medium text-gray-700">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      ) : (
        required && <span className="text-red-500">*</span>
      )}

      <div className="relative">
        <input
          id={id}
          className={cn(
            baseStyles,
            sizeStyles[size],
            search ? "pr-10" : "", // Add right padding for the icon
            className
          )}
          required={required}
          {...props}
        />
        {search && (
          <span className="absolute inset-y-0 right-3 flex items-center">
            <svg
              className="fill-gray-500 dark:fill-gray-400 w-5 h-5"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M3.04175 9.37363C3.04175 5.87693 5.87711 3.04199 9.37508 3.04199C12.8731 3.04199 15.7084 5.87693 15.7084 9.37363C15.7084 12.8703 12.8731 15.7053 9.37508 15.7053C5.87711 15.7053 3.04175 12.8703 3.04175 9.37363ZM9.37508 1.54199C5.04902 1.54199 1.54175 5.04817 1.54175 9.37363C1.54175 13.6991 5.04902 17.2053 9.37508 17.2053C11.2674 17.2053 13.003 16.5344 14.357 15.4176L17.177 18.238C17.4699 18.5309 17.9448 18.5309 18.2377 18.238C18.5306 17.9451 18.5306 17.4703 18.2377 17.1774L15.418 14.3573C16.5365 13.0033 17.2084 11.2669 17.2084 9.37363C17.2084 5.04817 13.7011 1.54199 9.37508 1.54199Z"
                fill=""
              />
            </svg>
          </span>
        )}
      </div>
      {validationMessage && (
        <ValidationMessage
          message={validationMessage}
          type={messageType ?? "error"}
        />
      )}
    </div>
  );
};

export default Input;
