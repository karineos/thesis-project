
let isRecording = false;
const microphone = document.getElementById('microphone');
const chatContainer = document.getElementById('chat_container');
const nameInput = document.getElementById('name_input');
const nameForm = document.getElementById('name_form');

let currentTranscript = '';

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = true;
recognition.continuous = true;

recognition.onresult = function(event) {
    let interimTranscript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
            currentTranscript += event.results[i][0].transcript;
        } else {
            interimTranscript += event.results[i][0].transcript;
        }
    }
    updateCurrentMessageBubble(currentTranscript + interimTranscript);
};

recognition.onend = function() {
    if (isRecording) {
        recognition.start();
    }
};

microphone.addEventListener('click', () => {
    if (isRecording) {
        recognition.stop();
        microphone.classList.remove('active');
        isRecording = false;
        sendFinalMessageBubble(currentTranscript);
        currentTranscript = ''; // Reset the transcript
    } else {
        recognition.start();
        microphone.classList.add('active');
        isRecording = true;
        createMessageBubble();
    }
});

function createMessageBubble() {
    const message = document.createElement('div');
    message.className = 'message user-message';
    message.id = 'current_message';
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateCurrentMessageBubble(text) {
    const message = document.getElementById('current_message');
    if (message) {
        message.textContent = text;
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
async function sendFinalMessageBubble(text) {
        const message = document.getElementById('current_message');
        if (message) {
            message.textContent = text;
            message.removeAttribute('id');

            // Send the message to the backend and get the response
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            // Append bot response to chat container
            appendMessage(data.response, 'bot-message');
            
            // Append emotion message
            if (data.emotion) {
                appendMessage(`The general felt emotion over the last 20 seconds is: ${data.emotion}`, 'bot-message');
            }
        }
    }


        function appendMessage(text, type) {
            const message = document.createElement('div');
            message.className = `message ${type}`;
            message.textContent = text;
            chatContainer.appendChild(message);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }


function handleInteraction() {
    var audio = new Audio('/output.mp3');
    audio.play();

    setTimeout(function() {
        nameInput.style.display = 'block';
        document.getElementById('submit_button').style.display = 'block';
        nameInput.focus();
    }, 6000);
}

document.addEventListener('DOMContentLoaded', function() {
    handleInteraction();

    nameForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const name = nameInput.value;

        // Simulate a response from the bot
        setTimeout(() => {
            appendMessage('Hello ' + name + '! How can I assist you today?', 'bot-message');
        }, 1000);

        const videoFeed = document.getElementById('video_feed');
        videoFeed.src = "{{ url_for('video_feed') }}?name=" + encodeURIComponent(name);
        videoFeed.style.maxWidth = "60%";
        videoFeed.style.width = "100%";
    });
});
