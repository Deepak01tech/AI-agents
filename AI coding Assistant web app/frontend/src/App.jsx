import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { 
  Send, Bot, User, Sparkles, MessageSquare, 
  Settings, ChevronDown, Check, Copy, PanelLeftClose, PanelLeft,
  Terminal, Globe, Wrench
} from 'lucide-react';
import './App.css';

// Generate a unique session ID
const generateSessionId = () => crypto.randomUUID();

// API call to the backend
const fetchChatResponse = async (message, sessionId) => {
  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed to fetch:", error);
    return { error: error.message || "Failed to connect to the assistant API" };
  }
};

// API call to clear session
const clearSessionApi = async (sessionId) => {
  try {
    await fetch('http://localhost:8000/api/clear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId }),
    });
  } catch (error) {
    console.error("Failed to clear session:", error);
  }
};

// Tool display name mapping
const toolDisplayInfo = {
  run_python_code: { label: 'Code Execution', icon: Terminal, color: '#2dd4bf' },
  web_search: { label: 'Web Search', icon: Globe, color: '#818cf8' },
};

// Custom renderer for code blocks in Markdown
const MarkdownComponents = {
  code({node, inline, className, children, ...props}) {
    const match = /language-(\w+)/.exec(className || '');
    const [copied, setCopied] = useState(false);
    
    const handleCopy = () => {
      navigator.clipboard.writeText(String(children).replace(/\n$/, ''));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    };

    return !inline && match ? (
      <div className="code-block-wrapper">
        <div className="code-header">
          <span className="code-header-lang">{match[1]}</span>
          <button className="copy-button" onClick={handleCopy} title="Copy code">
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
        <pre {...props} className={className}>
          <code className={className}>
            {children}
          </code>
        </pre>
      </div>
    ) : (
      <code className={className} {...props}>
        {children}
      </code>
    );
  }
};

function App() {
  const [messages, setMessages] = useState([]);
  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sessionId, setSessionId] = useState(generateSessionId);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = '44px';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = Math.min(scrollHeight, 200) + 'px';
    }
  }, [inputVal]);

  const handleSubmit = async (e) => {
    e?.preventDefault();
    
    if (!inputVal.trim() || isLoading) return;
    
    const userMsg = inputVal.trim();
    setInputVal('');
    
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);
    
    const response = await fetchChatResponse(userMsg, sessionId);
    
    setIsLoading(false);
    
    if (response.error) {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: `**Error:** ${response.error}\n\nMake sure the backend is running.`,
        tools_used: [],
      }]);
    } else {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: response.response,
        tools_used: response.tools_used || [],
      }]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const clearChat = async () => {
    await clearSessionApi(sessionId);
    const newId = generateSessionId();
    setSessionId(newId);
    setMessages([]);
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      {sidebarOpen && (
        <aside className="sidebar animate-fade-in">
          <div className="sidebar-header">
            <div className="logo-container">
              <Sparkles size={18} />
            </div>
            <span className="app-title">Nexus AI</span>
          </div>
          
          <div className="sidebar-content">
            <button className="new-chat-btn" onClick={clearChat}>
              <MessageSquare size={16} />
              New session
            </button>
            
            <div style={{ padding: '0 4px', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '8px', marginBottom: '8px' }}>
              AGENT CAPABILITIES
            </div>
            
            <div className="capability-item">
              <Wrench size={14} style={{ color: 'var(--accent)' }} />
              <span>Tool Use (Code & Search)</span>
            </div>
            <div className="capability-item">
              <MessageSquare size={14} style={{ color: 'var(--primary)' }} />
              <span>Conversation Memory</span>
            </div>
            <div className="capability-item">
              <Sparkles size={14} style={{ color: 'var(--secondary)' }} />
              <span>Multi-step Reasoning</span>
            </div>
            
            <div style={{ padding: '0 4px', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '16px', marginBottom: '8px' }}>
              CURRENT SESSION
            </div>

            {messages.length > 0 ? (
              <div className="history-item active">
                <MessageSquare size={14} />
                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {messages[0]?.content.substring(0, 30)}...
                </span>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                No active session
              </div>
            )}
            
            <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border)', paddingTop: '16px' }}>
              <div className="history-item">
                <Settings size={16} />
                Settings
              </div>
            </div>
          </div>
        </aside>
      )}

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="top-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button 
              className="icon-btn" 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              title={sidebarOpen ? "Close sidebar" : "Open sidebar"}
            >
              {sidebarOpen ? <PanelLeftClose size={20} /> : <PanelLeft size={20} />}
            </button>
            <div className="model-selector">
              <Sparkles size={14} style={{ color: 'var(--accent)' }} />
              <span>Nexus AI Agent v2.0</span>
              <ChevronDown size={14} />
            </div>
          </div>
          <div className="status-indicator">
            <div className="status-dot"></div>
            Online
          </div>
        </header>

        {/* Chat Area */}
        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome-screen">
              <div className="welcome-logo">
                <Sparkles size={40} color="white" />
              </div>
              <h1 className="welcome-title">How can I help you code?</h1>
              <p className="welcome-subtitle">
                I'm your AI coding agent. I can write & <strong>run code</strong>, <strong>search the web</strong>, and remember our full conversation.
              </p>
              
              <div className="suggestions-grid">
                <button className="suggestion-card" onClick={() => setInputVal("Run this Python code: print('Hello from Nexus AI!')")}>
                  <div className="suggestion-icon"><Terminal size={18} /></div>
                  <div className="suggestion-title">Execute Code</div>
                  <div className="suggestion-desc">Run a Python snippet live</div>
                </button>
                <button className="suggestion-card" onClick={() => setInputVal("Search the web for the latest Python version and show me the key features.")}>
                  <div className="suggestion-icon"><Globe size={18} /></div>
                  <div className="suggestion-title">Search the Web</div>
                  <div className="suggestion-desc">Get current information</div>
                </button>
                <button className="suggestion-card" onClick={() => setInputVal("My name is Deepak. Write and run a Python function that greets me by name.")}>
                  <div className="suggestion-icon"><MessageSquare size={18} /></div>
                  <div className="suggestion-title">Memory + Code</div>
                  <div className="suggestion-desc">Test memory and code execution</div>
                </button>
                <button className="suggestion-card" onClick={() => setInputVal("Design a RESTful API schema for a user authentication system with JWT tokens.")}>
                  <div className="suggestion-icon"><Sparkles size={18} /></div>
                  <div className="suggestion-title">Design Architecture</div>
                  <div className="suggestion-desc">Plan APIs and systems</div>
                </button>
              </div>
            </div>
          ) : (
            <div className="messages-wrapper">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  <div className={`avatar ${msg.role}`}>
                    {msg.role === 'ai' ? <Bot size={20} /> : <User size={20} />}
                  </div>
                  <div className="message-content">
                    {/* Tool badges */}
                    {msg.role === 'ai' && msg.tools_used && msg.tools_used.length > 0 && (
                      <div className="tool-badges">
                        {msg.tools_used.map((tool, i) => {
                          const info = toolDisplayInfo[tool] || { label: tool, icon: Wrench, color: '#94a3b8' };
                          const IconComponent = info.icon;
                          return (
                            <span key={i} className="tool-badge" style={{ borderColor: info.color + '40', color: info.color }}>
                              <IconComponent size={12} />
                              {info.label}
                            </span>
                          );
                        })}
                      </div>
                    )}
                    <div className="message-bubble markdown">
                      {msg.role === 'user' ? (
                        <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                      ) : (
                        <ReactMarkdown components={MarkdownComponents}>
                          {msg.content}
                        </ReactMarkdown>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="message ai">
                  <div className="avatar ai">
                    <Bot size={20} />
                  </div>
                  <div className="message-content">
                    <div className="message-bubble" style={{ display: 'inline-block', padding: '16px' }}>
                      <div className="thinking-label">
                        <Sparkles size={12} className="animate-pulse" />
                        Thinking & using tools...
                      </div>
                      <div className="typing-indicator" style={{ padding: 0, marginTop: '8px' }}>
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-area-container">
          <form className="input-box" onSubmit={handleSubmit}>
            <textarea
              ref={textareaRef}
              className="input-field"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything — I can run code and search the web... (Shift+Enter for new line)"
              rows={1}
            />
            <div className="input-toolbar">
              <div className="toolbar-actions">
                {/* Reserved space for file upload etc. */}
              </div>
              <button 
                type="submit" 
                className="send-btn"
                disabled={!inputVal.trim() || isLoading}
              >
                Send <Send size={16} />
              </button>
            </div>
          </form>
          <div className="input-footer">
            Nexus AI Agent • Memory enabled • Tools: Code Execution, Web Search
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
