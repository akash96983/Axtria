import React, { useState, useRef } from 'react';
import ChatWindow from '../components/ChatWindow';
import InputBox from '../components/InputBox';

export default function Home() {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Session ID Management
    const sessionIdRef = useRef(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleNewChat = () => {
        setMessages([]);
        sessionIdRef.current = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    };

    const handleSend = async (text) => {
        const userMsg = { text, sender: 'user' };
        setMessages(prev => [...prev, userMsg]);
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, session_id: sessionIdRef.current }),
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            const botMsg = { text: data.text, source: data.source, count: data.count, sender: 'bot' };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            console.error('Error fetching chat response:', error);
            setMessages(prev => [...prev, { text: "Sorry, I'm having trouble connecting to the server.", sender: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white relative">
            <ChatWindow messages={messages} isLoading={isLoading} onNewChat={handleNewChat} />
            <InputBox onSend={handleSend} disabled={isLoading} />
        </div>
    );
}
