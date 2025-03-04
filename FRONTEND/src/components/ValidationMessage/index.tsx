import React from "react";
import { cn } from "@/lib/utils";

export type ValidationMessageType = "info" | "success" | "warning" | "error";

interface ValidationMessageProps{
    message: string
    type: ValidationMessageType
}

const ValidationMessage:React.FC<ValidationMessageProps> =  ({message, type}) => {
    const baseStyle = "text-sm mt-1";
    const messageStyle = {
        error: "text-red-500",
        success: "text-green-500",
        info: "text-cyan-500",
        warning: "text-warning-500"
    }
    return (
        <p className={cn(baseStyle, undefined, undefined, messageStyle[type])}>{message}</p>
    )
}

export default ValidationMessage