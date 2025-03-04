import React from "react";

interface TabsProps {
  tabs: string[];
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, setActiveTab }) => {
  return (
    <div className="flex border-b border-gray-300 dark:border-gray-700 space-x-4">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => setActiveTab(tab)}
          className={`py-2 px-4 text-sm font-medium transition-all duration-300 ${
            activeTab === tab
              ? "border-b-2 border-blue-500 text-blue-600 dark:text-blue-400"
              : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-white"
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  );
};

export default Tabs;
