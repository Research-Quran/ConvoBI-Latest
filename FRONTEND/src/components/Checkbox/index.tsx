"use client";
import React from "react";
import { cn } from "@/lib/utils";

interface CheckboxOption {
  value: string | number;
  label?: string;
  disabled?: boolean;
}

interface CheckboxGroupProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "onChange"> {
  label?: string;
  options?: CheckboxOption[];
  selectedValues?: (string | number)[];
  onChange?: (value: string | number) => void;
  variant?: "success" | "error" | "warning" | "info" | "default";
  size?: "sm" | "md" | "lg";
  checkboxClassName?: string;
  labelClassName?: string;
}

const sizeStyles = {
  sm: "w-2 h-2 text-xs",
  md: "w-4 h-4 text-sm",
  lg: "w-6 h-6 text-lg",
};

const variantStyles = {
  success: "checked:bg-green-500 checked:border-green-500 focus:ring-green-500 accent-green-500",
  error: "checked:bg-red-500 checked:border-red-500 focus:ring-red-500 accent-red-500",
  warning: "checked:bg-yellow-500 checked:border-yellow-500 focus:ring-yellow-500 accent-yellow-500",
  info: "checked:bg-blue-500 checked:border-blue-500 focus:ring-blue-500 accent-blue-500",
  default: "checked:bg-blue-500 checked:border-blue-500 focus:ring-blue-500 accent-blue-500",
};


const CheckboxGroup: React.FC<CheckboxGroupProps> = ({
  label,
  options = [],
  selectedValues = [],
  onChange = () => {},
  variant = "default",
  size = "md",
  className = "",
  checkboxClassName = "",
  labelClassName = "",
  ...props
}) => {
  return (
    <div className={cn("p-2", className)} {...props}>
      {label && <label className="block text-sm font-medium text-gray-700 dark:text-gray-400 mb-2">{label}</label>}

      <div className="grid grid-cols-2 gap-x-4 gap-y-2">
        {options.map((option) => {
          const isChecked = selectedValues.includes(option.value);

          return (
            <label
              key={option.value}
              className={cn(
                "flex items-center space-x-3 cursor-pointer",
                option.disabled ? "opacity-60 cursor-not-allowed" : "",
                labelClassName
              )}
            >
              <input
                type="checkbox"
                className={cn(
                  "border-gray-300 rounded transition-all focus:ring-2 focus:outline-none",
                  "dark:bg-blue-800 dark:border-blue-600",
                  "disabled:cursor-not-allowed disabled:opacity-60",
                  sizeStyles[size],
                  variantStyles[variant], // Apply the color variant dynamically
                  checkboxClassName
                )}
                checked={isChecked}
                onChange={() => !option.disabled && onChange(option.value)}
                disabled={option.disabled}
                aria-checked={isChecked}
              />

              {option.label && (
                <span className={cn("text-gray-700 dark:text-gray-400 truncate", labelClassName)}>
                  {option.label}
                </span>
              )}
            </label>
          );
        })}
      </div>
    </div>
  );
};

export default CheckboxGroup;
