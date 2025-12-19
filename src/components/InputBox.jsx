import React, { useState, useEffect, useRef } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { clsx } from 'clsx';

export default function InputBox({ onSend, disabled }) {
    const [text, setText] = useState('');
    const inputRef = useRef(null);

    // Auto-focus on mount and when re-enabled
    useEffect(() => {
        if (!disabled) {
            inputRef.current?.focus();
        }
    }, [disabled]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (text.trim() && !disabled) {
            onSend(text);
            setText('');
        }
    };

    return (
        <div className="w-full bg-gradient-to-t from-surface-50 via-surface-50 to-transparent p-6 pb-8 sticky bottom-0 z-40">
            <div className="max-w-4xl mx-auto relative">
                <form
                    onSubmit={handleSubmit}
                    className={clsx(
                        "flex items-center gap-2 p-2 pl-5 bg-white rounded-2xl shadow-xl shadow-surface-300/30 border border-surface-200 transition-all duration-300",
                        "focus-within:shadow-primary-500/10 focus-within:border-primary-300 ring-4 ring-transparent focus-within:ring-primary-100"
                    )}
                >
                    <div className="text-primary-500">
                        <Sparkles className="w-5 h-5" />
                    </div>

                    <input
                        ref={inputRef}
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Ask a clinical trial question..."
                        className="flex-1 bg-transparent text-surface-900 placeholder:text-surface-400 text-sm py-2.5 focus:outline-none"
                        disabled={disabled}
                        autoFocus
                    />

                    <button
                        type="submit"
                        disabled={!text.trim() || disabled}
                        className={clsx(
                            "p-3 rounded-xl transition-all duration-200 flex items-center justify-center aspect-square",
                            !text.trim() || disabled
                                ? "bg-surface-100 text-surface-400 cursor-not-allowed"
                                : "bg-primary-600 text-white hover:bg-primary-700 shadow-lg shadow-primary-600/30 hover:scale-105 active:scale-95"
                        )}
                        aria-label="Send"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
                <div className="text-center mt-3 text-xs text-surface-400 font-medium">
                    AI can make mistakes. Please verify important information.
                </div>
            </div>
        </div>
    );
}
