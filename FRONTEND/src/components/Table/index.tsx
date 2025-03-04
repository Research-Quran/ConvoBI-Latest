'use client'
import React from "react";
import Spinner from "@/components/Spinner";

export interface ColumnProps<T extends Record<string, any>> {
    key: keyof T;
    label: string;
    render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface PaginationProps {
    current: number;
    pageSize: number
    total: number
    onChange: (page: number) => void
}

interface TableProps<T> {
    columns: {
        key: keyof T | string;
        label: string;
        render?: (value: T[keyof T], row: T) => React.ReactNode
    }[];
    dataSource: T[];
    onRowClick?: (row: T) => void;
    className?: string;
    pagination?: PaginationProps
    loading?: boolean
}

const Table = <T,>({ columns, dataSource, className, pagination, ...props }: TableProps<T>) => {
    const totalPages = pagination ? Math.ceil(pagination.total / pagination.pageSize) : 0;
    const maxButtons = 5;

    const getPageNumbers = () => {
        let pages = [];
        if (totalPages <= maxButtons + 2) {
            pages = Array.from({ length: totalPages }, (_, i) => i + 1);
        } else {
            pages = [1, 2, 3, 4, 5, "...", totalPages];
        }
        return pages;
    };

    return (
        <div className="my-5">
            <div className="max-w-full relative overflow-x-auto shadow-md sm:rounded-lg">
                {props.loading && (
                    <div className="absolute inset-0 bg-white bg-opacity-50 z-10"></div>
                )}
                <table className={`w-full text-sm text-left min-h-50 rtl:text-right text-gray-500 dark:text-gray-400 ${className}`}>
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            {columns.map((col) => (
                                <th key={col.key as string} scope="col" className="px-6 py-3">{col.label}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {dataSource.length > 0 && (props.loading === false || props.loading ===undefined) ? dataSource.map((row, rowIndex) => (
                            <tr
                                key={rowIndex}
                                className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600"
                                onClick={() => props.onRowClick && props.onRowClick(row)}
                            >
                                {columns.map((column) => (
                                    <td key={column.key as string} className="px-6 py-4">
                                        {column.render ? column.render(row[column.key as keyof T], row) : String(row[column.key as keyof T])}
                                    </td>
                                ))}
                            </tr>
                        )) : (
                            <tr>
                                <td colSpan={columns.length} className="text-center">
                                    <div role="status" className="absolute -translate-x-1/2 -translate-y-1/2 top-2/4 left-1/2">
                                        {props.loading === true ? (
                                            <Spinner />
                                        ) : (
                                            <div>
                                                <svg className="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                                    <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z" />
                                                </svg>
                                                <p>No Data</p>
                                            </div>
                                        )}
                                    </div>
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
            {pagination && pagination?.total > 0 && (
                <div className="flex flex-col items-end my-3">
                    <div className="flex items-center gap-2">
                        <span className="text-gray-600">
                            {`${(pagination.current - 1) * pagination.pageSize + 1}-${Math.min(
                                pagination.current * pagination.pageSize,
                                pagination.total
                            )} of ${pagination.total} items`}
                        </span>
                        <button
                            className={`px-3 py-1 border rounded ${pagination.current === 1 ? "text-gray-400 cursor-not-allowed" : "hover:bg-gray-100"
                                }`}
                            onClick={() => pagination.onChange(pagination.current - 1)}
                            disabled={pagination.current === 1}
                        >
                            Prev
                        </button>
                        {getPageNumbers().map((page) => (
                            <button
                                key={page}
                                className={`px-3 py-1 border rounded ${page === "..."
                                    ? "cursor-default text-gray-400"
                                    : page === pagination.current
                                        ? "bg-blue-500 text-white"
                                        : "hover:bg-gray-100"
                                    }`}
                                onClick={() => page !== "..." && pagination.onChange(Number(page))}
                                disabled={page === "..."}
                            >
                                {page}
                            </button>
                        ))}
                        <button
                            className={`px-3 py-1 border rounded ${pagination.current === totalPages ? "text-gray-400 cursor-not-allowed" : "hover:bg-gray-100"
                                }`}
                            onClick={() => pagination.onChange(pagination.current + 1)}
                            disabled={pagination.current === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}

        </div>

    )
}

export default Table