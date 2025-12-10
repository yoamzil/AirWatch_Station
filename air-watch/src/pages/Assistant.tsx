"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Send, Bot, User, Loader2, AlertCircle } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

// Change this to your backend URL
const BACKEND_URL = "http://localhost:5001";

const Assistant = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Hello! 👋 I'm your environmental health assistant.\n\nI can help you with:\n• Current air quality and sensor readings\n• Historical data and trends\n• Health recommendations based on conditions\n• Alerts and anomalies\n\nWhat would you like to know?"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check backend connection on mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      if (response.ok) {
        setIsBackendConnected(true);
        console.log("✅ Backend connected!");
      }
    } catch (error) {
      console.error("❌ Backend not connected:", error);
      setIsBackendConnected(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input.trim();
    setInput("");
    setIsLoading(true);

    try {
      // Call Python backend
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: currentInput })
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "Sorry, I couldn't process that request."
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsBackendConnected(true);
    } catch (error) {
      console.error("Error sending message:", error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "⚠️ I couldn't connect to the backend server.\n\n**Troubleshooting:**\n• Make sure the Python backend is running: `python app.py`\n• Check that it's running on http://localhost:5000\n• Make sure you're connected to 1337_GUEST WiFi\n• Try refreshing the page"
      };

      setMessages(prev => [...prev, errorMessage]);
      setIsBackendConnected(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      {/* Header */}
      <header className="flex items-center gap-4 px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
        <div className="flex items-center gap-2 flex-1">
          <div className="p-1.5 rounded-lg bg-blue-500/10">
            <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <h1 className="font-semibold text-slate-900 dark:text-slate-100">AI Health Advisor</h1>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isBackendConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-xs text-slate-600 dark:text-slate-400">
                {isBackendConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Connection Warning */}
      {!isBackendConnected && (
        <div className="mx-4 mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg flex items-start gap-2">
          <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-500 flex-shrink-0 mt-0.5" />
          <div className="text-sm">
            <p className="font-medium text-yellow-900 dark:text-yellow-200">Backend Not Connected</p>
            <p className="text-yellow-700 dark:text-yellow-300 mt-1">
              Make sure your Python backend is running: <code className="bg-yellow-100 dark:bg-yellow-900 px-1 py-0.5 rounded">python app.py</code>
            </p>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-300`}
          >
            {message.role === "assistant" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center">
                <Bot className="h-4 w-4 text-blue-600 dark:text-blue-400" />
              </div>
            )}
            <div
              className={`max-w-[85%] md:max-w-[75%] p-4 rounded-2xl shadow-sm ${
                message.role === "user"
                  ? "bg-blue-600 text-white rounded-br-md"
                  : "bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-bl-md border border-slate-200 dark:border-slate-700"
              }`}
            >
              <p className="text-sm md:text-base whitespace-pre-wrap leading-relaxed">{message.content}</p>
            </div>
            {message.role === "user" && (
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                <User className="h-4 w-4 text-white" />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 justify-start animate-in fade-in duration-300">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center">
              <Bot className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-4 rounded-2xl rounded-bl-md shadow-sm">
              <Loader2 className="h-5 w-5 animate-spin text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about air quality, health tips, or alerts..."
              className="flex-1 h-12 rounded-xl bg-slate-50 dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 focus-visible:ring-blue-500 focus-visible:border-blue-500"
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="h-12 w-12 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </Button>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 text-center">
            Try: "Is the air safe?" • "Show yesterday's data" • "Any alerts?" • "Health advice"
          </p>
        </div>
      </div>
    </div>
  );
};

export default Assistant;