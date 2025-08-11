document.getElementById("promptForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const prompt = document.getElementById("prompt").value.trim();
    if (!prompt) {
        alert("Please enter a prompt");
        return;
    }

    const responseDiv = document.getElementById("response");
    responseDiv.textContent = "Loading...";

    const formData = new FormData();
    formData.append("prompt", prompt);

    try {
        const res = await fetch("/prompt", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        responseDiv.textContent = data.response;
    } catch (error) {
        responseDiv.textContent = "Error: " + error.message;
    }
});
