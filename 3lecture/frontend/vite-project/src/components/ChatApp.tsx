import React, { useState, useRef, useEffect } from 'react';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

const LOCAL_STORAGE_KEY = 'grok_chat_history';

export const ChatApp: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (saved) {
      setMessages(JSON.parse(saved));
    }
  }, []);

  // Save chat history to localStorage on every update
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage: Message = { sender: 'user', text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setLoading(true);
    try {
      // Prepare chat history for backend (role: user/assistant)
      const historyForBackend = newMessages.map((msg) => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text,
      }));
      const response = await fetch('http://localhost:8000/assistant/openai_search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: historyForBackend }),
      });
      const data = await response.json();
      const botMessage: Message = { sender: 'bot', text: data.response };
      setMessages((msgs) => [...msgs, botMessage]);
    } catch (error) {
      setMessages((msgs) => [...msgs, { sender: 'bot', text: 'Ошибка при соединении с сервером.' }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div style={{
      background: '#18191A',
      width: '100vw',
      height: '100vh',
      minHeight: '100vh',
      minWidth: '100vw',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'Inter, Arial, sans-serif',
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 1000,
    }}>
      {/* Top right user avatar placeholder */}
      <div style={{
        position: 'absolute',
        top: 32,
        right: 48,
        zIndex: 10,
      }}>
        <div style={{
          width: 44,
          height: 44,
          borderRadius: '50%',
          background: '#23272f',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 700,
          fontSize: 18,
          textTransform: 'lowercase',
          letterSpacing: 1,
        }}>sa</div>
      </div>
      {/* Chat area */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        width: '',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: messages.length === 0 ? 'center' : 'flex-start',
        position: 'relative',
        paddingTop: 0,
        paddingBottom: 120,
      }}>
        <div style={{
          width: '100%',
          maxWidth: 600,
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 8,
        }}>
          {messages.length === 0 && (
            <div style={{ color: '#fff', opacity: 0.7, fontSize: 22, textAlign: 'center', marginTop: 80 }}>
              Похоже, запросов сообщений еще не было
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                alignItems: 'flex-end',
                gap: 12,
                width: '100%',
                justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                padding: '4px 0',
              }}
            >
              <div style={{
                width: 38,
                height: 38,
                borderRadius: '50%',
                background: msg.sender === 'user' ? '#3b82f6' : '#fbbf24',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontWeight: 700,
                fontSize: 20,
                flexShrink: 0,
                boxShadow: '0 2px 8px #0002',
              }}>
                {msg.sender === 'user' ? '🧑' : '🤖'}
              </div>
              <div style={{
                background: msg.sender === 'user' ? '#23272f' : '#23272f',
                color: msg.sender === 'user' ? '#fff' : '#fbbf24',
                borderRadius: 18,
                padding: '12px 18px',
                maxWidth: '80%',
                fontSize: 16,
                boxShadow: msg.sender === 'user' ? '0 2px 8px #3b82f633' : '0 2px 8px #fbbf2433',
                borderBottomRightRadius: msg.sender === 'user' ? 4 : 18,
                borderBottomLeftRadius: msg.sender === 'user' ? 18 : 4,
                wordBreak: 'break-word',
                textAlign: 'left',
              }}>
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, width: '100%', justifyContent: 'flex-start' }}>
              <div style={{
                width: 38,
                height: 38,
                borderRadius: '50%',
                background: '#fbbf24',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontWeight: 700,
                fontSize: 20,
                flexShrink: 0,
                boxShadow: '0 2px 8px #0002',
              }}>🤖</div>
              <div style={{ color: '#fbbf24', fontSize: 16 }}>Бот печатает...</div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      </div>
      {/* Input bar fixed at bottom */}
      <form
        onSubmit={e => {
          e.preventDefault();
          sendMessage();
        }}
        style={{
          background: '#23272f',
          width: '100vw',
          position: 'fixed',
          bottom: 0,
          left: 0,
          zIndex: 100,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px 0 24px 0',
          borderTop: '1px solid #23272f',
        }}
      >
        <div style={{
          width: '100%',
          maxWidth: 600,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Как Grok может помочь?"
            style={{
              width: '70%',
              minWidth: 180,
              maxWidth: 420,
              padding: '16px 20px',
              borderRadius: 18,
              border: 'none',
              outline: 'none',
              fontSize: 18,
              background: '#18191A',
              color: '#fff',
              marginRight: 12,
              boxShadow: '0 2px 8px #0002',
            }}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            style={{
              padding: '16px 32px',
              borderRadius: 18,
              border: 'none',
              background: '#fbbf24',
              color: '#23272f',
              fontWeight: 700,
              fontSize: 18,
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s',
              boxShadow: '0 2px 8px #fbbf2433',
            }}
          >
            {loading ? '...' : <span style={{fontWeight: 700}}>⏺</span>}
          </button>
        </div>
      </form>
    </div>
  );
};
