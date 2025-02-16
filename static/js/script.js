document.addEventListener('DOMContentLoaded', function() {
  const chatBody = document.getElementById('chatBody');
  const chatInput = document.getElementById('chatInput');
  const sendChatBtn = document.getElementById('sendChatBtn');

  if (!chatBody || !chatInput || !sendChatBtn) {
      console.error("Chatbot elements not found! Check HTML IDs.");
      return;
  }

  function addMessage(text, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('chat-message');
      messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
      messageDiv.innerText = text;
      chatBody.appendChild(messageDiv);
      chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll
  }

  function sendMessage() {
      const userMessage = chatInput.value.trim();
      if (!userMessage) return;

      addMessage(userMessage, 'user');
      chatInput.value = '';

      fetch('/chatbot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
          addMessage(data.reply, 'bot');
      })
      .catch(error => {
          addMessage('Error: Unable to process request.', 'bot');
          console.error(error);
      });
  }

  sendChatBtn.addEventListener('click', sendMessage);

  chatInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
          sendMessage();
      }
  });
});
