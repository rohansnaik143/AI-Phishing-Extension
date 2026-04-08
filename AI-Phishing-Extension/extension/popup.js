document.getElementById("checkBtn").addEventListener("click", function() {

    let url = document.getElementById("urlInput").value;
    let resultText = document.getElementById("resultText");
    let resultBox = document.getElementById("resultBox");

    resultText.innerText = "Checking...";
    resultBox.className = "checking";

    fetch("http://127.0.0.1:8000/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === 1) {
            resultText.innerText = "Phishing Detected";
            resultBox.className = "phishing";
        } else {
            resultText.innerText = "Safe Link";
            resultBox.className = "safe";
        }
    });
});