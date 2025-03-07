document.addEventListener("DOMContentLoaded", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab && tab.url.includes("youtube.com/")) {
        let videoId = null;

        if (tab.url.includes("watch?v=")) {
            videoId = new URL(tab.url).searchParams.get("v"); // Extract video ID for normal videos
        } else if (tab.url.includes("shorts/")) {
            const parts = tab.url.split("shorts/");
            if (parts.length > 1) {
                videoId = parts[1].split("?")[0];  // Extract video ID for Shorts
            }
        }

        if (!videoId) {
            alert("Could not extract video ID.");
            return;
        }

        fetch(`http://127.0.0.1:5000/transcript?video_id=${videoId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Transcript not available.");
                } else {
                    const transcriptText = encodeURIComponent(data.transcript); // URL encode transcript
                    const iframeUrl = `http://localhost:64767//?text=${transcriptText}`;
                    document.getElementById("transcriptFrame").src = iframeUrl; // Load inside popup
                }
            })
            .catch(error => console.error("Error fetching transcript:", error));
    } else {
        alert("Please open a YouTube video or Shorts.");
    }

    // Close button functionality
    document.getElementById("closeExtension").addEventListener("click", () => {
        window.close(); // Closes the popup when clicked
    });
});
