import React, { ReactNode, useState, useEffect } from "react";

interface ModalProps {
    isOpen: boolean;
    title?: string;
    onCancle: () => void;
    children: ReactNode;
    footer?: ReactNode;
    className?: string;
    size?: "sm" | "md" | "lg"
}

const Modal: React.FC<ModalProps> = ({ isOpen, title, onCancle, children, footer, className, size = "md" }) => {
    const [zIndex, setZindex] = useState<number>(99999)

    useEffect(() => {
        setZindex(prev => prev + 10)
    }, [isOpen])

    if (!isOpen) return null

    const sizeClasses: Record<string, string> = {
        sm: "max-w-md w-full",
        md: "max-w-2xl w-full",
        lg: "max-w-4xl w-full"
    };

    return (
        <div className={`fixed inset-0 flex items-center justify-center overflow-y-auto modal z-${zIndex} h-[calc(100%-1rem)]`}>
            <div className="fixed inset-0 h-full w-full bg-gray-400/20"></div>
            <div className={`relative w-full rounded-3xl bg-white  dark:bg-gray-900 ${sizeClasses[size] || sizeClasses['md']} p-5 lg:p-10`}>
                <div className="flex items-center justify-between pb-3 border-b rounded-t dark:border-gray-600 border-gray-200">
                    <button className="absolute right-3 top-3 z-999 flex h-9.5 w-9.5 items-center justify-center rounded-full bg-gray-100 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white sm:right-6 sm:top-6 sm:h-11 sm:w-11" onClick={() => onCancle()}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" clipRule="evenodd" d="M6.04289 16.5413C5.65237 16.9318 5.65237 17.565 6.04289 17.9555C6.43342 18.346 7.06658 18.346 7.45711 17.9555L11.9987 13.4139L16.5408 17.956C16.9313 18.3466 17.5645 18.3466 17.955 17.956C18.3455 17.5655 18.3455 16.9323 17.955 16.5418L13.4129 11.9997L17.955 7.4576C18.3455 7.06707 18.3455 6.43391 17.955 6.04338C17.5645 5.65286 16.9313 5.65286 16.5408 6.04338L11.9987 10.5855L7.45711 6.0439C7.06658 5.65338 6.43342 5.65338 6.04289 6.0439C5.65237 6.43442 5.65237 7.06759 6.04289 7.45811L10.5845 11.9997L6.04289 16.5413Z"
                                fill="currentColor"></path>
                        </svg>
                    </button>
                    {title && (
                        <h4 className="font-semibold text-gray-800 text-title-sm dark:text-white/90">{title}</h4>
                    )}
                </div>
                <div className="p-4 md:p-5 space-y-4">{children}</div>
                {footer && (
                    <div className="flex items-center justify-end w-full gap-3 mt-6">{footer}</div>
                )}
            </div>
        </div>
    )
}

export default Modal