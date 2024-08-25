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



  function sendMessage(event) {
    if (event.keyCode===13|| event.type === "click"){

   
    var inputElement = document.getElementById("messageInput");
    var message = inputElement.value;
  
    // Create a new div for the user's message
    var userBubble = document.createElement("div");
    userBubble.className = "chat-bubble user-bubble";
    userBubble.appendChild(document.createTextNode(message));
  
    // Append the user's message to the message list
    document.getElementById("messageList").appendChild(userBubble);
  
    // Clear the input field
    inputElement.value = "";
   // Scroll to the bottom of the message list
   document.getElementById("messageList").scrollTop = document.getElementById("messageList").scrollHeight;
    // Generate and append chatbot response after a delay
    setTimeout(function() {
      var response = generateResponse(message);
      var chatbotBubble = document.createElement("div");
      chatbotBubble.className = "chat-bubble chatbot-bubble";
      chatbotBubble.appendChild(document.createTextNode(response));
      document.getElementById("messageList").appendChild(chatbotBubble);

      document.getElementById("messageList").scrollTop = document.getElementById("messageList").scrollHeight;
    }, 1000); // Delay in milliseconds
  }
}
  
  function generateResponse(message) {
    // Your chatbot logic here
    if (message.toLowerCase().includes("hello")) {
      return "Hi there!";
    } else if (message.toLowerCase().includes("how are you")) {
      return "I'm good, thank you for asking!";
    } else {
      return "I'm sorry, I didn't understand that.";
    }
  }


  
  function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "navbar") {
      x.className += " responsive";
    } else {
      x.className = "navbar";
    }
  }