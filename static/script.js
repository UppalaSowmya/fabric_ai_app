console.log("JS LOADED");

function startRecording() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Your browser does not support Speech Recognition ❌");
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.start();

    recognition.onstart = function() {
        alert("🎤 Recording started");
    };

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        alert("You said: " + text);

        fetch("/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("fabric").value = data.fabric;
            document.getElementById("gsm").value = data.gsm;
            document.getElementById("color").value = data.color;
            document.getElementById("quantity").value = data.quantity;
            document.getElementById("delivery").value = data.delivery;
        });
    };

    recognition.onerror = function(event) {
        alert("Error: " + event.error);
    };
}