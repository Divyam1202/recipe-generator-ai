import { useState, useEffect, useRef } from "react";
import "./App.css";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [ingredients, setIngredients] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateRecipe = async () => {
    if (!ingredients.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: "user",
      content: ingredients,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIngredients("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ ingredients: userMessage.content })
      });

      if (!res.ok) throw new Error("Failed to generate recipe");

      const data = await res.json();
      
      // Fetch image
      const ingredientsList = userMessage.content.split(",")[0].trim();
      let recipeImage = "";
      try {
        const imageRes = await fetch(
          `https://api.unsplash.com/search/photos?query=${ingredientsList}%20food&count=1&client_id=kmL92F3P3aQDkr7Xd01fRhKH_aXaOc0kKYvtJTRHaXk`
        );
        const imageData = await imageRes.json();
        if (imageData.results && imageData.results.length > 0) {
          recipeImage = imageData.results[0].urls.regular;
        }
      } catch (err) {
        console.log("Could not fetch image");
      }

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        type: "ai",
        content: data.recipe,
        image: recipeImage,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Update conversation list
      const conversationTitle = userMessage.content.substring(0, 30) + "...";
      if (!currentConversationId) {
        const newConvId = Date.now();
        setCurrentConversationId(newConvId);
        setConversations(prev => [{
          id: newConvId,
          title: conversationTitle,
          timestamp: new Date(),
          messages: [userMessage, aiMessage]
        }, ...prev]);
      } else {
        setConversations(prev => prev.map(conv =>
          conv.id === currentConversationId
            ? { ...conv, messages: [...conv.messages, userMessage, aiMessage] }
            : conv
        ));
      }

    } catch (err) {
      setError("Failed to generate recipe. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      generateRecipe();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setCurrentConversationId(null);
    setIngredients("");
  };

  const loadConversation = (convId) => {
    const conv = conversations.find(c => c.id === convId);
    if (conv) {
      setCurrentConversationId(convId);
      setMessages(conv.messages);
    }
  };

  const deleteConversation = (convId, e) => {
    e.stopPropagation();
    setConversations(prev => prev.filter(c => c.id !== convId));
    if (currentConversationId === convId) {
      startNewConversation();
    }
  };

  const clearAllConversations = () => {
    if (window.confirm("Clear all conversations?")) {
      setConversations([]);
      startNewConversation();
    }
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
        <div className="sidebar-header">
          <h2 className="sidebar-title">🍳 RecipeAI</h2>
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? "⊗" : "☰"}
          </button>
        </div>

        <button className="new-chat-btn" onClick={startNewConversation}>
          <span>+ New Chat</span>
        </button>

        {/* Conversations History */}
        <div className="conversations-section">
          <div className="conversations-label">History</div>
          <div className="conversations-list">
            {conversations.length === 0 ? (
              <div className="empty-state">No conversations yet</div>
            ) : (
              conversations.map(conv => (
                <div
                  key={conv.id}
                  className={`conversation-item ${currentConversationId === conv.id ? "active" : ""}`}
                  onClick={() => loadConversation(conv.id)}
                >
                  <div className="conversation-title">{conv.title}</div>
                  <button
                    className="delete-conv-btn"
                    onClick={(e) => deleteConversation(conv.id, e)}
                    aria-label="Delete conversation"
                  >
                    ✕
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Sidebar Footer */}
        {conversations.length > 0 && (
          <div className="sidebar-footer">
            <button className="clear-btn" onClick={clearAllConversations}>
              🗑️ Clear History
            </button>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className="main-container">
        {/* Chat Area */}
        <div className="chat-area">
          {/* Empty State */}
          {messages.length === 0 && (
            <div className="empty-chat-state">
              <div className="welcome-section">
                <div className="welcome-emoji">🍳</div>
                <h1 className="welcome-title">RecipeAI Chef</h1>
                <p className="welcome-subtitle">Your personal AI chef ready to create amazing recipes</p>
                
                <div className="features-showcase">
                  <div className="feature">
                    <span className="feature-icon">🥘</span>
                    <div className="feature-text">
                      <h3>Smart Recipes</h3>
                      <p>AI-powered recipes from any ingredient</p>
                    </div>
                  </div>
                  <div className="feature">
                    <span className="feature-icon">⚡</span>
                    <div className="feature-text">
                      <h3>Instant Results</h3>
                      <p>Get recipes in seconds</p>
                    </div>
                  </div>
                  <div className="feature">
                    <span className="feature-icon">📸</span>
                    <div className="feature-text">
                      <h3>Food Photos</h3>
                      <p>Beautiful images for inspiration</p>
                    </div>
                  </div>
                </div>

                <div className="suggestion-prompts">
                  <p className="prompt-label">Try asking:</p>
                  <button
                    className="prompt-btn"
                    onClick={() => setIngredients("chicken, garlic, onions, tomato")}
                  >
                    "chicken, garlic, onions"
                  </button>
                  <button
                    className="prompt-btn"
                    onClick={() => setIngredients("pasta, cream, mushrooms, butter")}
                  >
                    "pasta, cream, mushrooms"
                  </button>
                  <button
                    className="prompt-btn"
                    onClick={() => setIngredients("rice, eggs, soy sauce, vegetables")}
                  >
                    "rice, eggs, vegetables"
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="messages-container">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`message ${msg.type === "user" ? "user-message" : "ai-message"}`}
              >
                {msg.type === "ai" && (
                  <div className="message-avatar">🤖</div>
                )}
                
                <div className="message-content">
                  {msg.type === "ai" && msg.image && (
                    <div className="message-image">
                      <img src={msg.image} alt="Recipe" />
                    </div>
                  )}
                  
                  <div className={`message-bubble ${msg.type === "user" ? "user-bubble" : "ai-bubble"}`}>
                    <div className="message-text">{msg.content}</div>
                    
                    {msg.type === "ai" && (
                      <div className="message-actions">
                        <button
                          className="action-btn"
                          onClick={() => {
                            navigator.clipboard.writeText(msg.content);
                            alert("Recipe copied!");
                          }}
                          title="Copy recipe"
                        >
                          📋 Copy
                        </button>
                        <button
                          className="action-btn"
                          onClick={() => {
                            setIngredients("");
                            setMessages([]);
                          }}
                          title="New recipe"
                        >
                          🔄 New
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {msg.type === "user" && (
                  <div className="message-avatar user-avatar">👤</div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message ai-message">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="ai-bubble loading-bubble">
                    <span className="cooking-pot">🍲</span>
                    <span className="loading-text">Cooking up your recipe...</span>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="message ai-message">
                <div className="message-avatar">⚠️</div>
                <div className="message-content">
                  <div className="ai-bubble error-bubble">{error}</div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              className="message-input"
              placeholder="Tell me your ingredients... (Ctrl+Enter to send)"
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              rows="3"
            />
            <button
              className="send-btn"
              onClick={generateRecipe}
              disabled={loading || !ingredients.trim()}
              aria-label="Generate recipe"
            >
              {loading ? (
                <span className="spinner"></span>
              ) : (
                "✈️"
              )}
            </button>
          </div>
          <p className="input-hint">RecipeAI can make mistakes. Always review recipes carefully.</p>
        </div>
      </main>
    </div>
  );
}