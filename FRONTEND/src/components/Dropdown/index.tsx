import { cn } from "@/lib/utils";
import React, { useState } from "react";
import ValidationMessage, { ValidationMessageType } from "../ValidationMessage";

interface DropDownProps {
  name: string;
  options: { value: string; label: string }[]; // Accepts objects for better flexibility
  onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  className?: string;
  disabled?: boolean;
  required?: boolean;
  label?: string;
  id?: string; // Optional id for accessibility  
  defaultValue?: string;
  variant?: "default" | "outline" | "error" | "success"; // Add variant prop
  size?: "sm" | "md" | "lg"; // Add size prop
validationMessage?: string;
  messageType?: ValidationMessageType;  

}

const baseStyles =
  "block w-full rounded-md transition-all duration-200 focus:outline-none focus:ring";

const variantStyles: Record<string, string> = {
  default: "border-gray-300 bg-white text-gray-900 focus:ring-blue-400",
  outline: "border border-gray-400 bg-transparent text-gray-700 focus:ring-gray-500",
  error: "border-red-500 bg-red-100 text-red-900 focus:ring-red-400",
  success: "border-green-500 bg-green-100 text-green-900 focus:ring-green-400",
};

const sizeStyles: Record<string, string> = {
  sm: "px-3 py-1 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-5 py-3 text-lg",
};

const DropDown: React.FC<DropDownProps> = ({
  name,
  options,
  onChange,
  className = "",
  disabled = false,
  required = false,
  label,
  id = `dropdown-${name}`,
  defaultValue = "",
  variant = "default",
  size = "md",
  validationMessage,
  messageType,
}) => {

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    
    if (onChange) {
      onChange(event);
    }
  };

  return (
    <div className="flex flex-col">
      {label ? (
        <label htmlFor={id} className="text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      ): (
        required && <span className="text-red-500">*</span>
      )}
      <select
        id={id}
        name={name}
        onChange={handleChange}
        onBlur={handleChange} // Validate on blur
        className={cn(
          baseStyles,
          // variantStyles[hasError ? "error" : variant],
          sizeStyles[size],
          className
        )}
        disabled={disabled}
        required={required}
        defaultValue={defaultValue}
      >
        <option value="" disabled hidden>
          Select {label || name.charAt(0).toUpperCase() + name.slice(1)}
        </option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {validationMessage && (
        <ValidationMessage
          message={validationMessage}
          type={messageType ?? "error"}
        />
      )}
    </div>
  );
};

export default DropDown;
