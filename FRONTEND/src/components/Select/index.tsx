import React from "react";
import { cn } from "@/lib/utils";
import ValidationMessage, {ValidationMessageType} from "../ValidationMessage";

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
    options: { value: string; label: string }[];
    label?: string;
    varient?: "default" | "primary" | "secondary" | "outlined";
    selectSize?: "sm" | "md" | "lg";
    validationMessage?: string;
    messageType?: ValidationMessageType
}

const Select: React.FC<SelectProps> = ({ options, label, varient = "default", selectSize = "md", className, validationMessage, messageType, ...props }) => {

    const baseStyles = `h-11 w-full appearance-none rounded-lg border border-${validationMessage ? 'red-500' : 'gray-300'} bg-transparent px-5 py-3 pr-11 text-sm shadow-theme-xs placeholder:text-gray-400 focus:border-${validationMessage ? 'red-500' : 'brand-300'} focus:outline-none focus:ring focus:ring-${validationMessage ? 'red-500/10' : 'brand-500/10'} dark:border-gray-700 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-${validationMessage ? 'red-500' : 'brand-800'} text-gray-400 dark:text-gray-400 bg-gray-50 dark:bg-gray-800`;

    const variantStyles = {
        default: `bg-white border-gray-300 text-gray-700`,
        primary: `bg-blue-500 text-white border-blue-500`,
        secondary: `bg-gray-200 text-gray-800 border-gray-400`,
        outlined: `bg-transparent border-2 text-gray-700 border-gray-300`,
    };

    const sizeStyles = {
        sm: "px-2 py-1 text-sm",
        md: "px-3 py-2 text-base",
        lg: "px-4 py-3 text-lg",
    };

    return (
        <div className="mb-4.5">
            {label ? (
                <label htmlFor={props.name} className="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    {label}
                    {props.required && <span className="text-red-500">*</span>}
                </label>
            ) : (
                props.required && <span className="text-red-500">*</span>
            )}

            <div className="relative z-20 bg-transparent dark:bg-form-input">
                <select
                    className={cn(baseStyles, variantStyles[varient], sizeStyles[selectSize], `${props.value !== "" ? `text-black dark:text-white ${className}` : className}`)}
                    {...props}
                >
                    {options.map((option) => (
                        <option key={option.value} value={option.value} className="text-gray-700 dark:bg-gray-900 dark:text-gray-400">
                            {option.label}
                        </option>
                    ))}
                </select>

                <span className="absolute right-4 top-1/2 z-30 -translate-y-1/2">
                    <svg
                        className="fill-current"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g opacity="0.8">
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M5.29289 8.29289C5.68342 7.90237 6.31658 7.90237 6.70711 8.29289L12 13.5858L17.2929 8.29289C17.6834 7.90237 18.3166 7.90237 18.7071 8.29289C19.0976 8.68342 19.0976 9.31658 18.7071 9.70711L12.7071 15.7071C12.3166 16.0976 11.6834 16.0976 11.2929 15.7071L5.29289 9.70711C4.90237 9.31658 4.90237 8.68342 5.29289 8.29289Z"
                                fill=""
                            ></path>
                        </g>
                    </svg>
                </span>
                {validationMessage && <ValidationMessage message={validationMessage} type={messageType ?? "error"} />}
            </div>
        </div>
    )
}

export default Select