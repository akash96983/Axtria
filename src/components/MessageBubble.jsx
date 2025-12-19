import React from 'react';
import SourceBadge from './SourceBadge';
import { Bot, User } from 'lucide-react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

export default function MessageBubble({ message }) {
    const isBot = message.sender === 'bot';

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={clsx("flex w-full mb-6 gap-3", isBot ? 'justify-start' : 'justify-end')}
        >
            {/* Avatar for Bot */}
            {isBot && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center text-white shadow-sm mt-1">
                    <Bot className="w-5 h-5" />
                </div>
            )}

            <div
                className={clsx(
                    "max-w-[85%] sm:max-w-[75%] p-4 text-sm leading-relaxed shadow-sm relative group",
                    isBot
                        ? 'bg-white border border-surface-200 text-surface-700 rounded-2xl rounded-tl-none'
                        : 'bg-gradient-to-br from-primary-600 to-primary-700 text-white rounded-2xl rounded-tr-none shadow-md shadow-primary-500/20'
                )}
            >
                {!isBot && (
                    <div className="absolute -right-2 top-0 w-2 h-2 overflow-hidden">
                        <div className="w-4 h-4 bg-primary-700 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
                    </div>
                )}

                <div className="whitespace-pre-wrap">
                    {message.text}
                </div>

                {isBot && message.source && (
                    <div className="mt-3 pt-2 border-t border-surface-100">
                        <SourceBadge source={message.source} count={message.count} />
                    </div>
                )}
            </div>

            {/* Avatar for User */}
            {!isBot && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-surface-200 flex items-center justify-center text-surface-500 mt-1">
                    <User className="w-5 h-5" />
                </div>
            )}
        </motion.div>
    );
}
