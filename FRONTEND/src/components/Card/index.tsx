import React, { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface CardProps {
    title?: string | null;
    children: ReactNode;
    className?: string
}

const Card: React.FC<CardProps> = ({ title,className, children }) => {
    const baseStyle = "rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]"
    return (
        <div className={cn(baseStyle, undefined, undefined, className )}>
            {title && (
                <div className="px-6 py-5">
                    <h3 className="text-base font-medium text-gray-800 dark:text-white/90">{title}</h3>
                </div>
            )}
            <div className="p-4 border-t border-gray-100 dark:border-gray-800 sm:p-6">{children}</div>
        </div>
    )
}

export default Card
