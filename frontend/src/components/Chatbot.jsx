import { useState, useRef, useEffect } from 'react';
import { fetchChatResponse } from '../utils/api';

export default function Chatbot({ defaultCity = 'Mumbai' }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am the FutureLens AI assistant. Ask me about ICU beds, hospital capacity, or disease outbreaks in any city. (e.g. "What is the ICU capacity in Bengaluru?")' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { sender: 'user', text: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await fetchChatResponse(userMessage, defaultCity);
      setMessages(prev => [...prev, { 
        sender: 'bot', 
        text: data.response || "I couldn't process that request." 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: "Error connecting to AI backend." }]);
    }
    
    setIsLoading(false);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-primary text-on-primary rounded-full shadow-[0_0_20px_rgba(34,211,238,0.4)] flex items-center justify-center hover:scale-105 active:scale-95 transition-all z-50"
      >
        <span className="material-symbols-outlined text-3xl">
          {isOpen ? 'close' : 'smart_toy'}
        </span>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-80 md:w-96 h-[500px] glass-panel rounded-xl flex flex-col overflow-hidden z-50 shadow-2xl border border-primary/20 animate-in">
          {/* Header */}
          <div className="p-4 border-b border-white/5 bg-surface-container-high flex items-center gap-3">
            <span className="material-symbols-outlined text-primary">smart_toy</span>
            <div>
              <h3 className="font-headline-md text-[16px] text-on-surface">FutureLens AI</h3>
              <p className="text-[10px] text-primary animate-pulse">Powered by XGBoost Model</p>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-4 bg-surface-dim/50">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-lg text-sm ${
                  msg.sender === 'user' 
                    ? 'bg-primary text-on-primary rounded-tr-none' 
                    : 'bg-surface-variant text-on-surface rounded-tl-none border border-white/5'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-surface-variant text-on-surface p-3 rounded-lg rounded-tl-none border border-white/5 text-sm flex gap-1">
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></span>
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-white/5 bg-surface-container-low">
            <form onSubmit={handleSend} className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about ICU predictions..."
                className="flex-1 bg-surface-dim border border-white/10 rounded-lg px-3 py-2 text-sm text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
              />
              <button 
                type="submit" 
                disabled={isLoading || !input.trim()}
                className="bg-primary/20 text-primary p-2 rounded-lg hover:bg-primary/30 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <span className="material-symbols-outlined">send</span>
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
