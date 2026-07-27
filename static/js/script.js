let allSymptoms = [];
let selectedSymptoms = [];

const searchInput = document.getElementById("symptom-search");
const suggestionsBox = document.getElementById("symptom-suggestions");
const selectedContainer = document.getElementById("selected-symptoms");
const predictButton = document.getElementById("predict-button");
const errorMessage = document.getElementById("error-message");

const loadingSection = document.getElementById("loading-section");
const resultSection = document.getElementById("result-section");

const predictedDisease = document.getElementById("predicted-disease");
const predictionConfidence = document.getElementById("prediction-confidence");
const healthGuidance = document.getElementById("health-guidance");


/* --------------------------------------------------
   Load symptoms from Flask
-------------------------------------------------- */

async function loadSymptoms() {
    try {
        const response = await fetch("/api/symptoms");

        if (!response.ok) {
            throw new Error("Unable to load symptoms.");
        }

        const data = await response.json();

        allSymptoms = data.symptoms;

    } catch (error) {
        errorMessage.textContent =
            "Unable to load symptom list. Please refresh the page.";
    }
}

loadSymptoms();


/* --------------------------------------------------
   Search symptoms
-------------------------------------------------- */

searchInput.addEventListener("input", function () {

    const query = searchInput.value.trim().toLowerCase();

    suggestionsBox.innerHTML = "";

    if (!query) {
        suggestionsBox.style.display = "none";
        return;
    }

    const matches = allSymptoms
        .filter(symptom =>
            symptom.toLowerCase().includes(query) &&
            !selectedSymptoms.includes(symptom)
        )
        .slice(0, 10);

    if (matches.length === 0) {
        suggestionsBox.style.display = "none";
        return;
    }

    matches.forEach(symptom => {

        const item = document.createElement("div");

        item.className = "suggestion-item";
        item.textContent = symptom;

        item.addEventListener("click", function () {
            addSymptom(symptom);
        });

        suggestionsBox.appendChild(item);
    });

    suggestionsBox.style.display = "block";
});


/* --------------------------------------------------
   Add symptom
-------------------------------------------------- */

function addSymptom(symptom) {

    if (!selectedSymptoms.includes(symptom)) {
        selectedSymptoms.push(symptom);
    }

    searchInput.value = "";
    suggestionsBox.style.display = "none";

    renderSelectedSymptoms();
}


/* --------------------------------------------------
   Remove symptom
-------------------------------------------------- */

function removeSymptom(symptom) {

    selectedSymptoms = selectedSymptoms.filter(
        item => item !== symptom
    );

    renderSelectedSymptoms();
}


/* --------------------------------------------------
   Display selected symptoms
-------------------------------------------------- */

function renderSelectedSymptoms() {

    selectedContainer.innerHTML = "";

    if (selectedSymptoms.length === 0) {

        const message = document.createElement("p");

        message.id = "no-symptoms-message";
        message.textContent = "No symptoms selected.";

        selectedContainer.appendChild(message);

        return;
    }

    selectedSymptoms.forEach(symptom => {

        const tag = document.createElement("div");

        tag.className = "symptom-tag";

        const text = document.createElement("span");
        text.textContent = symptom;

        const removeButton = document.createElement("button");

        removeButton.className = "remove-symptom";
        removeButton.type = "button";
        removeButton.textContent = "×";

        removeButton.addEventListener("click", function () {
            removeSymptom(symptom);
        });

        tag.appendChild(text);
        tag.appendChild(removeButton);

        selectedContainer.appendChild(tag);
    });
}


/* --------------------------------------------------
   Close suggestions when clicking outside
-------------------------------------------------- */

document.addEventListener("click", function (event) {

    if (
        !searchInput.contains(event.target) &&
        !suggestionsBox.contains(event.target)
    ) {
        suggestionsBox.style.display = "none";
    }
});


/* --------------------------------------------------
   Predict disease
-------------------------------------------------- */

predictButton.addEventListener("click", async function () {

    errorMessage.textContent = "";

    if (selectedSymptoms.length === 0) {

        errorMessage.textContent =
            "Please select at least one symptom.";

        return;
    }

    resultSection.hidden = true;
    loadingSection.hidden = false;

    predictButton.disabled = true;

    try {

        const response = await fetch("/api/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                symptoms: selectedSymptoms
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Prediction failed."
            );
        }

        predictedDisease.textContent =
            data.prediction.disease;

        predictionConfidence.textContent =
            `${data.prediction.confidence}%`;

        displayGuidance(data.guidance);

        resultSection.hidden = false;

        resultSection.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        errorMessage.textContent =
            error.message ||
            "Unable to process your request.";

    } finally {

        loadingSection.hidden = true;
        predictButton.disabled = false;
    }
});


/* --------------------------------------------------
   Format Gemini guidance
-------------------------------------------------- */

function displayGuidance(guidance) {
    let formatted = guidance
        // Horizontal divider
        .replace(/^\s*\*{3}\s*$/gm, "<hr>")

        // Markdown headings
        .replace(/^###\s+(.+)$/gm, "<h3>$1</h3>")

        // Bold text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")

        // Italic text
        .replace(/\*(.*?)\*/g, "<em>$1</em>")

        // Bullet points
        .replace(/^\s*[\*\-]\s+(.+)$/gm, "<li>$1</li>")

        // Line breaks
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");

    healthGuidance.innerHTML = formatted;
}