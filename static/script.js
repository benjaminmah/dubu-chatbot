// Global variable to store the selected ingredients
var selectedIngredients = [];
var selectedFile = null;
var chatMessages = []; // Global variable to store the chat messages

function toggleIngredient(element) {
  element.classList.toggle("selected");

  // Get the text content of the ingredient button
  var ingredient = element.textContent.trim();

  // Check if the ingredient is already in the selectedIngredients array
  var index = selectedIngredients.indexOf(ingredient);
  if (index > -1) {
    // If the ingredient is already selected, remove it from the array
    selectedIngredients.splice(index, 1);
  } else {
    // If the ingredient is not selected, add it to the array
    selectedIngredients.push(ingredient);
  }
}

function handleFileSelect(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];
  const fileNameElement = fileInput.parentNode.querySelector('.file-name');

  // Check if the selected file is a PDF
  if (file.type !== 'application/pdf') {
    alert('Only PDF files are allowed.');
    fileInput.value = ''; // Clear the file input
    fileNameElement.textContent = 'No file chosen';
    return;
  }

  // Update the selectedFile variable
  selectedFile = file;

  // Update the file name element with the selected file name
  fileNameElement.textContent = file.name;
}

function startCooking() {
  // Check if a file is selected
  if (!selectedFile) {
    alert('Please upload a file before starting cooking.');
    return;
  }

  // Check if ingredients are selected
  if (selectedIngredients.length === 0) {
    alert('Please select at least one ingredient before starting cooking.');
    return;
  }

  // Disable all buttons
  var buttons = document.querySelectorAll('button');
  buttons.forEach(function(button) {
    button.disabled = true;
  });

  // Add a loading animation to the Start Cooking button
  var startButton = document.querySelector('.start-button');
  startButton.innerHTML = '<span class="loading-indicator"></span> Loading...';

  // Create a FormData object to store the data
  var formData = new FormData();
  formData.append('file', selectedFile); // Append the selected file
  formData.append('selectedIngredients', JSON.stringify(selectedIngredients)); // Append the selected ingredients

  // Make an AJAX request to the Python server
  fetch('/start-cooking', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(result => {
      // Process the response from the server
      console.log(result.message);

      // Redirect to a new HTML file
      window.location.href = '/new-page'; // Replace 'new-page.html' with the desired file name
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
  const userMessageInput = document.getElementById('user-message');
  const sendButton = document.getElementById('send-button');
  const clearButton = document.getElementById('clear-button');

  // Send message on Enter key press
  userMessageInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent the default form submission
      sendMessage();
    }
  });

  // Send message on button click
  sendButton.addEventListener('click', function() {
    sendMessage();
  });

  // Clear chat on button click
  clearButton.addEventListener('click', function() {
    clearChat();
  });

  function sendMessage() {
    const message = userMessageInput.value;
    if (message.trim() !== '') {
      appendUserMessage(message);
      sendUserMessageToPython(message); // Send the user message to Python
      userMessageInput.value = '';
    }
  }

  function appendLoadingIndicator() {
    const chatLog = document.querySelector('.chat-log');
    const chatMessage = document.createElement('div');
    chatMessage.classList.add('chat-message', 'chatbot-message');
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content', 'loading-message');
    const loadingIndicator = document.createElement('div');
    loadingIndicator.classList.add('loading-indicator');
    loadingIndicator.textContent = '.';
    messageContent.appendChild(loadingIndicator);
    chatMessage.appendChild(messageContent);
    chatLog.appendChild(chatMessage);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
  }

  function sendUserMessageToPython(message) {
    // Create an object with the user message data
    const userMessageData = {
      message: message,
      chatMessages: chatMessages
    };

    // Append the loading indicator to the chat log
    appendLoadingIndicator();

    let loadingTimeout;
    let loadingCount = 0;
    const loadingIndicator = document.querySelector('.loading-indicator');

    // Function to update the loading indicator text
    function updateLoadingIndicator() {
      loadingCount++;
      const dotsCount = loadingCount % 4;
      const loadingIndicator = document.querySelector('.loading-indicator');
      const dots = '.'.repeat(dotsCount);
      loadingIndicator.textContent = dots;
      loadingIndicator.classList.add('show'); // Show the loading indicator
    }

    // Function to start the loading animation
    function startLoadingAnimation() {
      loadingTimeout = setInterval(updateLoadingIndicator, 200);
    }

    // Function to stop the loading animation
    function stopLoadingAnimation() {
      clearInterval(loadingTimeout);
    }

    // Start the loading animation
    startLoadingAnimation();

    // Delay the actual request by 0.5 seconds
    setTimeout(() => {
      // Make an AJAX request to the Python server
      fetch('/pass-user-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userMessageData)
      })
        .then(response => response.json())
        .then(result => {
          // Process the response from the server
          console.log(result.answer);

          // Stop the loading animation
          stopLoadingAnimation();

          // Remove the loading indicator
          removeLoadingIndicator();

          // Append the chatbot's response to the chat log
          appendChatBotMessage(result.answer);

          // Save the messages to the chat history
          chatMessages.push({"role": "user", "content": message });
          chatMessages.push({"role": "assistant", "content": result.answer });
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }, 500); // Delay the request by 0.5 seconds
  }

  function removeLoadingIndicator() {
    const loadingMessage = document.querySelector('.chat-log .loading-message');
    if (loadingMessage) {
      loadingMessage.remove();
    }
  }

  function appendUserMessage(message) {
    const chatLog = document.querySelector('.chat-log');
    const chatMessage = document.createElement('div');
    chatMessage.classList.add('chat-message', 'user-message'); // Add the 'user-message' class
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    chatMessage.appendChild(messageContent);
    chatLog.appendChild(chatMessage);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
  }

  function appendChatBotMessage(message) {
    const chatLog = document.querySelector('.chat-log');
    const chatMessage = document.createElement('div');
    chatMessage.classList.add('chat-message', 'chatbot-message'); // Add the 'chatbot-message' class
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    chatMessage.appendChild(messageContent);
    chatLog.appendChild(chatMessage);
    chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
  }

  function clearChat() {
    const chatLog = document.querySelector('.chat-log');
    chatLog.innerHTML = ''; // Clear the chat log
    chatMessages = []; // Clear the chat history
  }
});

// Add event listener to the Start Cooking button
const startButton = document.querySelector('.start-button');
startButton.addEventListener('click', startCooking);
