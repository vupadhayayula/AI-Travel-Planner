function updateDurationValue(value) {
    document.getElementById("durationValue").innerText = value;
}

function generatePlan() {
    // Show loading message before making the API request
    let responseElement = document.getElementById("response");
    responseElement.innerHTML = "Generating your travel plan... ⏳";
    
    // Collect user input
    const travelData = {
        travelType: document.getElementById("travelType").value,
        interests: document.getElementById("interests").value,
        season: document.getElementById("season").value,
        tripDuration: document.getElementById("duration").value,
        budgetRange: document.getElementById("budget").value
    };

    // Send POST request to Flask backend
    fetch("/generate-plan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(travelData)
    })
    .then(response => response.json())
    .then(data => {
        // Display AI response
        responseElement.innerHTML = `<strong>AI Travel Plan:</strong><br>${data.plan}`;
    })
    .catch(error => {
        responseElement.innerHTML = `<span style="color: red;">Error generating travel plan. Please try again.</span>`;
        console.error("Error:", error);
    });
}
