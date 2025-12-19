import React from 'react';

export default function Logs() {
    const [logs, setLogs] = React.useState([]);

    React.useEffect(() => {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        fetch(`${apiBaseUrl}/api/logs`)
            .then(res => res.json())
            .then(data => setLogs(data))
            .catch(err => console.error("Failed to load logs", err));
    }, []);

    return (
        <div className="h-full overflow-y-auto max-w-5xl mx-auto p-8">
            <h2 className="text-2xl font-bold text-slate-800 mb-6">Chat Turn Logs</h2>

            <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 table-auto">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Time</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Query</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200 text-sm md:text-base">
                        {logs.map((log) => (
                            <tr key={log.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap text-gray-500 text-xs">{log.timestamp}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${log.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                        {log.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-gray-500 font-mono text-xs break-all min-w-[200px]">{log.source}</td>
                                <td className="px-6 py-4 text-gray-900 break-words min-w-[300px]">{log.query}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
