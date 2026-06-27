// =============================
// FastAPI Backend URL
// =============================

const API_URL = "http://127.0.0.1:8000";

// =============================
// Predict Disease
// =============================

async function predictDisease(imageFile) {

    try {

        const formData = new FormData();

        formData.append("file", imageFile);

        const response = await fetch(`${API_URL}/predict`, {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Prediction Failed");

        }

        const data = await response.json();

        return data;

    }

    catch(error){

        console.error(error);

        alert("Backend connection failed!");

        return null;

    }

}