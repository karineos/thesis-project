document.addEventListener("DOMContentLoaded", function () {
    const textElement = document.getElementById("typing-text");
    const text = textElement.textContent;
    textElement.textContent = "";

    let index = 0;
    const speed = 30; // typing speed in milliseconds

    function type() {
        if (index < text.length) {
            textElement.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    }

    type();
});
