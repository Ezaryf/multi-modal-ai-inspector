import React, { useState, useEffect, useRef } from 'react';
import './ChatPanel.css';

export default function ChatPanel({ mediaId, initialHistory = [] }) {
    const [messages, setMessages] = useState(initialHistory);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        loadChatHistory();
    }, [mediaId]);

    const loadChatHistory = async () => {
        try {
            const { api } = await import('../services/api');
            const history = await api.getChatHistory(mediaId);
            setMessages(history);
        } catch (error) {
            console.error('Failed to load chat history:', error);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const question = input.trim();
        setInput('');

        // Add user message immediately
        const userMsg = {
            role: 'user',
            message: question,
            created_at: new Date().toISOString(),
        };

        setMessages(prev => [...prev, userMsg]);
        setLoading(true);

        try {
            const { api } = await import('../services/api');
            const response = await api.askQuestion(mediaId, question);

            const assistantMsg = {
                role: 'assistant',
                message: response.answer,
                created_at: new Date().toISOString(),
                sources: response.sources,
            };

            setMessages(prev => [...prev, assistantMsg]);
        } catch (error) {
            console.error('Ask failed:', error);

            const errorMsg = {
                role: 'assistant',
                message: 'Sorry, I encountered an error processing your question.',
                created_at: new Date().toISOString(),
            };

            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="chat-panel">
            <h2 className="panel-title gradient-text">💬 Ask Questions</h2>

            <div className="chat-container">
                <div className="messages-container">
                    {messages.length === 0 && (
                        <div className="empty-state">
                            <p>No messages yet. Ask a question about your media!</p>
                        </div>
                    )}

                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`message ${msg.role}`}
                        >
                            <div className="message-header">
                                <span className="message-role">
                                    {msg.role === 'user' ? '👤 You' : '🤖 Inspector'}
                                </span>
                                <span className="message-time">
                                    {new Date(msg.created_at).toLocaleTimeString()}
                                </span>
                            </div>
                            <div className="message-content">
                                {msg.message}
                            </div>
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="message-sources">
                                    <span className="sources-label">Sources:</span>
                                    {msg.sources.map((source, i) => (
                                        <span key={i} className="source-badge">{source}</span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}

                    {loading && (
                        <div className="message assistant">
                            <div className="message-header">
                                <span className="message-role">🤖 Inspector</span>
                            </div>
                            <div className="message-content typing">
                                <span className="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </span>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                <div className="chat-input-container">
                    <input
                        type="text"
                        className="chat-input"
                        placeholder="Ask a question about this media..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        disabled={loading}
                    />
                    <button
                        className="btn btn-primary send-button"
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                    >
                        {loading ? '...' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    );
}
