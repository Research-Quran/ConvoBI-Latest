"use client";
import React from "react";
import { cn } from "@/lib/utils";

interface RadioButtonOption {
  value: boolean | string | number;
  label: string;
  disabled?: boolean;
}

interface RadioButtonGroupProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "onChange"> {
  label?: string;
  options?: RadioButtonOption[];
  selectedValue?: boolean | string | number;
  onChange?: (value: boolean | string | number) => void;
  size?: "sm" | "md" | "lg";
  name?: string;
  variant?: "success" | "error" | "warning" | "info" | "default";
}

const variantStyles = {
  default: "border-blue-600 bg-blue-600", 
  success: "border-green-500 bg-green-500", 
  error: "border-red-500 bg-red-500", 
  warning: "border-yellow-500 bg-yellow-500", 
  info: "border-teal-500 bg-teal-500", 
};

const baseStyles = "flex items-center cursor-pointer transition-all duration-200 font-medium p-2";

const sizeStyles = {
  sm: "px-3 py-1 text-sm space-x-2",
  md: "px-4 py-2 text-base space-x-3",
  lg: "px-5 py-3 text-lg space-x-4",
};

const RadioButtonGroup: React.FC<RadioButtonGroupProps> = ({
  label,
  options = [{ value: "default", label: "Default" }],
  selectedValue,
  onChange = () => {},
  size = "md",
  className,
  name,
  variant = "default", 
  ...props
}) => {
  return (
    <div className={cn("mb-4", className)} {...props}>
      {label && <label className="font-semibold dark:text-gray-700">{label}</label>}

      <div className="flex items-center space-x-3">
        {options.map((option) => {
          const isSelected = selectedValue === option.value;
          const isDisabled = option.disabled;

          return (
            <div
              key={option.value.toString()}
              onClick={() => !isDisabled && onChange(option.value)}
              className={cn(
                baseStyles,
                sizeStyles[size],
                isDisabled ? "opacity-50 cursor-not-allowed" : "hover:text-blue-500"
              )}
            >
              <div
                className={cn(
                  "flex h-5 w-5 items-center justify-center rounded-full border-[1.25px]",
                  isSelected ? variantStyles[variant] : "border-gray-400 bg-transparent hover:border-blue-600 hover:bg-gray-200"
                )}
              >
                {isSelected && <span className="h-2.5 w-2.5 rounded-full bg-white"></span>}
              </div>

              <span className={cn("ml-2 text-gray-800 dark:text-gray-300", isDisabled ? "opacity-50" : "")}>
                {option.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RadioButtonGroup;
