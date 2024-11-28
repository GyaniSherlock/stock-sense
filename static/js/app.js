document.getElementById("send-button").addEventListener("click", function () {
    const userInput = document.getElementById("user-input").value.trim();
    const chatBody = document.getElementById("chat-body");

    if (userInput !== "") {
        // Add user's message to chat body
        const userMessage = document.createElement("div");
        userMessage.className = "message user";
        userMessage.textContent = userInput;
        chatBody.appendChild(userMessage);

        // Scroll to the latest message
        chatBody.scrollTop = chatBody.scrollHeight;

        // Make an AJAX request to the Flask server
        fetch('/process_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })
        })
            .then(response => response.json())
            .then(data => {
                // Add bot's response to the chat body
                const botMessage = document.createElement("div");
                botMessage.className = "message bot";
                botMessage.innerHTML = data.response; // Allow HTML in response
                chatBody.appendChild(botMessage);

                // Scroll to the latest message
                chatBody.scrollTop = chatBody.scrollHeight;

                // Clear the input field
                document.getElementById("user-input").value = "";
            })
            .catch(error => console.error('Error:', error));
    }
});

document.getElementById("clear-chat").addEventListener("click", function () {
    document.getElementById("chat-body").innerHTML = "";
});
