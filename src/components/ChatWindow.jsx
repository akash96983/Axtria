import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import { Bot, Sparkles, TrendingUp, Plus } from 'lucide-react';
import { motion } from 'framer-motion';

export default function ChatWindow({ messages, isLoading, onNewChat }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    return (
        <div className="flex-1 relative flex flex-col min-h-0 bg-white">
            <div className="flex-1 overflow-y-auto px-4 scroll-smooth">
                {messages.length > 0 && (
                    <div className="sticky top-0 z-30 flex justify-end pt-4 pb-2 bg-gradient-to-b from-white via-white/80 to-transparent -mx-4 px-8 mb-4">
                        <button
                            onClick={onNewChat}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-surface-200 rounded-xl text-sm font-medium text-surface-600 hover:text-primary-600 hover:border-primary-300 hover:shadow-lg transition-all shadow-sm active:scale-95"
                        >
                            <Plus className="w-4 h-4" />
                            New Chat
                        </button>
                    </div>
                )}
                <div className={`max-w-4xl mx-auto min-h-full flex flex-col ${messages.length === 0 ? 'justify-center' : 'justify-start'}`}>
                    {messages.length === 0 ? (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex flex-col items-center justify-center text-center px-6"
                        >
                            <div className="relative mb-12">
                                <div className="absolute inset-0 bg-primary-100 blur-[100px] opacity-30 rounded-full" />
                                <div className="relative">
                                    <h1 className="text-5xl font-extrabold text-slate-900 tracking-tight leading-tight mb-4">
                                        Trial Intelligence
                                    </h1>
                                    <p className="text-slate-500 text-lg max-w-lg mx-auto leading-relaxed font-medium">
                                        Deep insights from clinical documentation and structured data, simplified for you.
                                    </p>
                                </div>
                            </div>

                            <div className="flex flex-wrap justify-center gap-2 max-w-xl">
                                {[
                                    "Summarize trials",
                                    "Phase III Diabetes",
                                    "Adverse Events",
                                    "Inclusion Criteria"
                                ].map((prompt, i) => (
                                    <button key={i} className="px-5 py-2.5 bg-white border border-slate-200 hover:border-primary-400 hover:text-primary-600 text-slate-600 rounded-full text-xs font-semibold shadow-sm transition-all hover:shadow-md active:scale-95">
                                        {prompt}
                                    </button>
                                ))}
                            </div>
                        </motion.div>
                    ) : (
                        <div className="space-y-6 pt-8 pb-4">
                            {messages.map((msg, idx) => (
                                <MessageBubble key={idx} message={msg} />
                            ))}

                            {isLoading && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex w-full mb-6 justify-start gap-3"
                                >
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center mt-1">
                                        <Bot className="w-5 h-5 text-white" />
                                    </div>
                                    <div className="bg-white border border-surface-200 rounded-2xl rounded-tl-none p-4 shadow-sm flex items-center gap-2">
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                        <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"></div>
                                    </div>
                                </motion.div>
                            )}
                            <div ref={bottomRef} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
