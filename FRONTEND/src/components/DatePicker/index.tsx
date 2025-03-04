import React, { useEffect, useRef, useState } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { cn } from "@/lib/utils";
import ValidationMessage, { ValidationMessageType } from "../ValidationMessage";

interface DatePickerProps {
  value?: string;
  onChange?: (date: string) => void;
  placeholder?: string;
  dateFormat?: string;
  className?: string;
  disabled?: boolean;
  required?: boolean;
  label?: string;
  id?: string;
  variant?: "default" | "outline" | "error" | "success";
  size?: "sm" | "md" | "lg";
validationMessage?: string;
  messageType?: ValidationMessageType;
}

const DatePicker: React.FC<DatePickerProps> = ({
  value,
  onChange,
  placeholder = "Select date",
  dateFormat = "M j, Y",
  className = "",
  disabled = false,
  required = false,
  label,
  id = `datepicker-${Math.random().toString(36).substr(2, 9)}`,
  variant = "default",
  size = "md",
  messageType,
  validationMessage
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!inputRef.current) return;

    const fp = flatpickr(inputRef.current, {
      mode: "single",
      static: true,
      monthSelectorType: "static",
      dateFormat,
      defaultDate: value,
      onChange: (selectedDates) => {
        const selectedDate = selectedDates[0]?.toISOString().split("T")[0] || "";
        // setHasError(required && !selectedDate);
        if (onChange) onChange(selectedDate);
      },
    });

    return () => {
      fp.destroy();
    };
  }, [value, onChange, dateFormat, required]);


  const baseStyles =
    "h-11 w-full rounded-lg border appearance-none px-4 py-2.5 text-sm shadow-theme-xs placeholder:text-gray-400 focus:outline-none focus:ring bg-transparent text-gray-800 border-gray-300 focus:border-brand-300 focus:ring-brand-500/20";

  const variantStyles = {
    default: "border-gray-300 bg-white text-gray-900 focus:ring-blue-400",
    outline: "border border-gray-400 bg-transparent text-gray-700 focus:ring-gray-500",
    error: "border-red-500 bg-red-100 text-red-900 focus:ring-red-400",
    success: "border-green-500 bg-green-100 text-green-900 focus:ring-green-400",
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
          ref={inputRef}
          type="text"
          className={cn(
            baseStyles,
            sizeStyles[size],
            "pr-10",
            className
          )}
          placeholder={placeholder}
          disabled={disabled}
          readOnly
          required={required}
        />
        <span className="absolute inset-y-0 right-3 flex items-center">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path
              d="M15.7504 2.9812H14.2879V2.36245C14.2879 2.02495 14.0066 1.71558 13.641 1.71558C13.2754 1.71558 12.9941 1.99683 12.9941 2.36245V2.9812H4.97852V2.36245C4.97852 2.02495 4.69727 1.71558 4.33164 1.71558C3.96602 1.71558 3.68477 1.99683 3.68477 2.36245V2.9812H2.25039C1.29414 2.9812 0.478516 3.7687 0.478516 4.75308V14.5406C0.478516 15.4968 1.26602 16.3125 2.25039 16.3125H15.7504C16.7066 16.3125 17.5223 15.525 17.5223 14.5406V4.72495C17.5223 3.7687 16.7066 2.9812 15.7504 2.9812Z"
              fill="#64748B"
            />
          </svg>
        </span>
      </div>
      {validationMessage && (
        <ValidationMessage
          message={validationMessage}
          type={messageType ?? "error"}
        />
      )}    </div>
  );
};

export default DatePicker;
