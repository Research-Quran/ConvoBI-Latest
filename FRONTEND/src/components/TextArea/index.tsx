import React from "react";
import { cn } from "@/lib/utils";
import ValidationMessage, {ValidationMessageType} from "../ValidationMessage";

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    className?: string;
    label?: string;
    required?: boolean;
    validationMessage?: string
    messageType?: ValidationMessageType
}

const TextArea: React.FC<TextAreaProps> = ({ className, label, required,validationMessage, messageType, ...props }) => {
    const baseStyles = `w-full rounded-lg border px-4 py-2.5 text-sm shadow-theme-xs focus:outline-none  bg-gray-50 dark:bg-gray-800  bg-transparent text-gray-900 dark:text-gray-300 text-gray-900 ${validationMessage ? 'border-red-300' :'border-gray-300'} focus:border-${validationMessage ? 'red-500': 'brand-300'} focus:ring focus:ring-${validationMessage ? 'red-500/10':'brand-500/10'} dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-${validationMessage ? 'red-800':'brand-800'}`;
    return (
        <div className="col-span-2">
            {label ? (
                <label htmlFor={props.name} className="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    {label}
                    {required && <span className="text-red-500">*</span>}
                </label>
            ): (
                required && (
                    <span className="text-red-500">*</span>
                )
            )}
            <div className="relative">
                <textarea
                    rows={props.rows ?? 6}
                    className={cn(baseStyles, undefined, undefined, className)}
                    {...props}
                ></textarea>
                {validationMessage && <ValidationMessage message={validationMessage} type={messageType ?? "error"} />}
            </div>
        </div>
    )
}

export default TextArea