const API_URL = "http://127.0.0.1:8000/chat";
const session_id = "user_" + Math.floor(Math.random() * 10000);

function toggleChat() {
    const chat = document.getElementById("chatContainer");
    const isVisible = chat.style.display === "flex";
    chat.style.display = isVisible ? "none" : "flex";
    
    if (!isVisible) {
        document.getElementById("userInput").focus();
    }
}

function appendMessage(role, text, isUser = false) {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatBox.appendChild(messageDiv);
    
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator(show) {
    const indicator = document.getElementById("typingIndicator");
    indicator.style.display = show ? "block" : "none";
    
    if (show) {
        const chatBox = document.getElementById("chatBox");
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");
    const text = input.value.trim();
    
    if (!text) return;

    // Disable input and button
    input.disabled = true;
    sendBtn.disabled = true;
    
    // Show user's message
    appendMessage("You", text, true);
    input.value = "";

    // Show typing indicator
    showTypingIndicator(true);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: session_id,
                query: text
            }),
        });

        const data = await response.json();
        
        // Hide typing indicator
        showTypingIndicator(false);
        
        // Show AI response
        const responseText = data.response || "Sorry, I didn't understand that.";
        appendMessage("AI Assistant", responseText, false);
        
        // Handle crisis detection
        if (data.crisis_detected) {
            setTimeout(() => {
                appendMessage("AI Assistant", "I've provided some crisis resources above. Would you like to talk about what you're experiencing right now? I'm here to listen and support you.", false);
            }, 1000);
        }
        
    } catch (error) {
        showTypingIndicator(false);
        appendMessage("AI Assistant", "⚠️ I'm having trouble connecting right now. Please try again in a moment, or consider reaching out to a crisis helpline if you need immediate support.", false);
        console.error("Chatbot error:", error);
    } finally {
        // Re-enable input and button
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize chat with welcome message delay
document.addEventListener('DOMContentLoaded', function() {
    // Add some interactive elements
    setTimeout(() => {
        const chatBox = document.getElementById("chatBox");
        if (chatBox.children.length === 1) { // Only the initial message
            setTimeout(() => {
                appendMessage("AI Assistant", "You can ask me about coping strategies, mental health resources, or just tell me what's on your mind. I'm here to help! 🌟", false);
            }, 2000);
        }
    }, 1000);
});

// Add scroll effect to header
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(44, 82, 130, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))';
        header.style.backdropFilter = 'none';
    }
});