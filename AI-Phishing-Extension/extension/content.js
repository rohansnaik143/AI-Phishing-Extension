let tooltip = document.createElement("div");
tooltip.id = "phishing-tooltip";
tooltip.style.position = "fixed";
tooltip.style.display = "none";
tooltip.style.zIndex = "999999";
document.body.appendChild(tooltip);

let cache = {};
let currentLink = null;
let hoverTimeout = null;

// Track mouse movement for tooltip positioning
document.addEventListener("mousemove", (e) => {
    if (tooltip.style.display === "block") {
        tooltip.style.top = e.clientY + 15 + "px";
        tooltip.style.left = e.clientX + 15 + "px";
    }
});

// Detect hover using mouseover (works on dynamic pages)
document.addEventListener("mouseover", function (e) {
    const link = e.target.closest("a");

    if (!link || !link.href) {
        hideTooltip();
        return;
    }

    currentLink = link;
    clearTimeout(hoverTimeout);

    hoverTimeout = setTimeout(() => {
        checkLink(link.href);
    }, 300); // small delay to avoid spam calls
});

document.addEventListener("mouseout", function (e) {
    if (e.target.closest("a")) {
        hideTooltip();
    }
});

function checkLink(url) {

    tooltip.style.display = "block";
    tooltip.textContent = "Checking...";
    tooltip.className = "checking";

    if (cache[url]) {
        updateTooltip(cache[url]);
        return;
    }

    fetch("http://127.0.0.1:8000/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        const status = data.status === 1 ? "phishing" : "safe";
        cache[url] = status;
        updateTooltip(status);
    })
    .catch(() => {
        tooltip.textContent = "Error";
        tooltip.className = "phishing";
    });
}

function updateTooltip(status) {
    if (status === "phishing") {
        tooltip.textContent = "🔴 Phishing Link!";
        tooltip.className = "phishing";
    } else {
        tooltip.textContent = "🟢 Safe Link";
        tooltip.className = "safe";
    }
}

function hideTooltip() {
    tooltip.style.display = "none";
}

// 🔴 Block phishing click
document.addEventListener("click", function (e) {
    const link = e.target.closest("a");
    if (!link || !link.href) return;

    if (cache[link.href] === "phishing") {
        e.preventDefault();
        showWarningOverlay(link.href);
    }
}, true);

function showWarningOverlay(url) {
    const overlay = document.createElement("div");
    overlay.id = "phishing-overlay";

    overlay.innerHTML = `
        <div class="warning-box">
            <h2>⚠ Dangerous Website Blocked</h2>
            <p>This link was detected as phishing:</p>
            <p class="url">${url}</p>
            <div class="buttons">
                <button id="goBack">Go Back</button>
                <button id="proceed">Proceed Anyway</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    document.getElementById("goBack").onclick = () => overlay.remove();
    document.getElementById("proceed").onclick = () => window.location.href = url;
}