const syncPointer = ({ x: pointerX, y: pointerY }) => {
    const x = pointerX.toFixed(2)
    const y = pointerY.toFixed(2)
    const xp = (pointerX / window.innerWidth).toFixed(2)
    const yp = (pointerY / window.innerHeight).toFixed(2)
    document.documentElement.style.setProperty('--x', x)
    document.documentElement.style.setProperty('--xp', xp)
    document.documentElement.style.setProperty('--y', y)
    document.documentElement.style.setProperty('--yp', yp)
  }
  document.body.addEventListener('pointermove', syncPointer)



document.getElementById("messageForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission
  
    var userMessage = document.getElementById("userMessage").value.trim(); // Trim whitespace
  
    if (userMessage === "") {
      // Handle empty message (optional)
      return;
    }
  
    fetch("/process_message", {
      method: "POST",
      body: JSON.stringify({ message: userMessage }),
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then(response => response.text())
    .then(data => {
      // Display the response from the Python script (test.py) in the chat container
      var chatMessage = document.createElement("div");
      chatMessage.textContent = data;
      document.getElementById("chatContainer").appendChild(chatMessage);
    })
    .catch(error => {
      console.error("Error:", error);
    });
  
    // Clear the input field after sending the message
    document.getElementById("userMessage").value = "";
  });
  