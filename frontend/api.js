// =============================
// FastAPI Backend URL
// =============================

const API_URL = "http://127.0.0.1:8003";

// =============================
// Predict Disease API
// =============================

async function predictDisease(imageFile) {

    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        throw new Error("Prediction Failed");
    }

    return await response.json();
}

// =============================
// Chat API
// =============================

async function askAI(question) {

    const response = await fetch(`${API_URL}/shetimitra`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })

    });

    if (!response.ok) {
        throw new Error("Chat Failed");
    }

    return await response.json();
}