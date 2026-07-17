// ==========================
// HTML Elements
// ==========================

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");

const predictBtn = document.getElementById("predictBtn");

const diseaseName = document.getElementById("disease");
const confidence = document.getElementById("confidence");

const description = document.getElementById("description");

const progressBar = document.getElementById("progressBar");

// ==========================
// Preview Image
// ==========================

imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) return;

    preview.src = URL.createObjectURL(file);

    preview.style.display = "block";

});


///===================================
//  sugarcane ai
//=================================
// ==========================
// Shetimitra Chat
// ==========================

const askBtn = document.getElementById("askBtn");

askBtn.addEventListener("click", async () => {

    const question = document.getElementById("question").value;

    if(question.trim() === ""){
        alert("Please enter a question.");
        return;
    }

    try{

        const data = await askAI(question);

        document.getElementById("answer").innerHTML =
            data.answer;

    }
    catch(error){

        console.error(error);

        document.getElementById("answer").innerHTML =
            "Unable to connect to AI Agent.";

    }

});

// ==========================
// Predict Button
// ==========================

predictBtn.addEventListener("click", async () => {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please choose an image.");

        return;

    }

    predictBtn.innerHTML = "Predicting...";

    const result = await predictDisease(file);

    predictBtn.innerHTML = "Predict Disease";

    if (!result) return;

    //------------------------

    const prediction = result[0];

    diseaseName.innerHTML = prediction.disease;

    confidence.innerHTML = prediction.confidence + "%";

    progressBar.style.width = prediction.confidence + "%";

    //------------------------

    const info = diseaseData[prediction.disease];

    if (!info) {

        description.innerHTML = "No information available.";

        return;

    }

    description.innerHTML = `

        <h3>Description</h3>

        <p>${info.description}</p>

        <br>

        <h3>Symptoms</h3>

        <ul>

        ${info.symptoms.map(s => `<li>${s}</li>`).join("")}

        </ul>

        <br>

        <h3>Treatment</h3>

        <ul>

        ${info.treatment.map(s => `<li>${s}</li>`).join("")}

        </ul>

        <br>

        <h3>Prevention</h3>

        <ul>

        ${info.prevention.map(s => `<li>${s}</li>`).join("")}

        </ul>

    `;

    diseaseName.style.color = info.color;

});