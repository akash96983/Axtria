import React from 'react';

export default function About() {
    return (
        <div className="max-w-3xl mx-auto p-6 space-y-6">
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">About This Chatbot</h2>
                <p className="text-slate-700 leading-relaxed">
                    This chatbot answers clinical trial questions using two fixed sources:
                </p>
                <ul className="list-disc list-inside space-y-2 text-slate-700 ml-4 font-mono text-sm bg-gray-50 p-4 rounded border border-gray-200">
                    <li>Pharma_Clinical_Trial_Notes.docx</li>
                    <li>Pharma_Clinical_Trial_AllDrugs.xlsx</li>
                </ul>
            </section>

            <section className="space-y-4">
                <h3 className="text-xl font-semibold text-slate-800">Key Principles</h3>
                <div className="grid gap-4 md:grid-cols-2">
                    <div className="p-4 bg-blue-50 border border-blue-100 rounded-lg">
                        <h4 className="font-semibold text-blue-900 mb-2">Grounded Responses</h4>
                        <p className="text-sm text-blue-800">Answers are strictly derived from the provided documents. No external knowledge is used.</p>
                    </div>
                    <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                        <h4 className="font-semibold text-slate-800 mb-2">No Medical Advice</h4>
                        <p className="text-sm text-slate-600">This system is for informational use only and does not replace professional medical judgment.</p>
                    </div>
                    <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                        <h4 className="font-semibold text-slate-800 mb-2">Explicit Citation</h4>
                        <p className="text-sm text-slate-600">Every claim is backed by a specific source file to ensure auditability.</p>
                    </div>
                    <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                        <h4 className="font-semibold text-slate-800 mb-2">Transparent Limits</h4>
                        <p className="text-sm text-slate-600">The system clearly states when information is missing rather than guessing.</p>
                    </div>
                </div>
            </section>

            <div className="text-center pt-8 text-sm text-gray-500 italic">
                This system is intended for informational and educational use only.
            </div>
        </div>
    );
}
