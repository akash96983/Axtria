import React from 'react';
import { FileText, Database, FileSpreadsheet } from 'lucide-react';
import { clsx } from 'clsx';

export default function SourceBadge({ source, count }) {
    const getIcon = (src) => {
        if (src.toLowerCase().includes('pdf') || src.toLowerCase().includes('doc')) return FileText;
        if (src.toLowerCase().includes('excel') || src.toLowerCase().includes('csv')) return FileSpreadsheet;
        return Database;
    };

    const Icon = getIcon(source);

    return (
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 mt-2 bg-surface-100 border border-surface-200 rounded-full text-xs font-medium text-surface-600 hover:bg-surface-200 transition-colors cursor-pointer select-none">
            <Icon className="w-3.5 h-3.5 text-primary-600" />
            <span className="" title={source}>{source}</span>
            {count > 0 && (
                <span className="flex items-center justify-center bg-primary-100 text-primary-700 w-4 h-4 rounded-full text-[10px] font-bold">
                    {count}
                </span>
            )}
        </div>
    );
}

