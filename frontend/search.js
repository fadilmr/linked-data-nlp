document.getElementById("submitButton").addEventListener("click", function () {
    const queryInput = document.getElementById("queryInput").value;

    fetch("http://localhost:8000/execute-query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: queryInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from backend:", data);

        const resultContainer = document.getElementById("resultContainer");
        resultContainer.innerHTML = "";

        if (data.data) {
            for (const item of data.data) {
                const div = document.createElement("div");
                div.className = "grid-item"; 
                
                // Check if the item has an object
                if (item.object) {
                    // Create a link for the subject
                    const subjectLink = document.createElement("a");
                    subjectLink.href = `details.html?title=${encodeURIComponent(item.subject)}`; // Pass subject as query parameter
                    subjectLink.textContent = item.subject;
                    subjectLink.className = "hover:text-blue-500"; // Add hover effect class
                    
                    // Create a paragraph for the object
                    const objectParagraph = document.createElement("p");
                    objectParagraph.textContent = item.object;
                    
                    // Append subject link and object paragraph to the div
                    div.appendChild(subjectLink);
                    div.appendChild(objectParagraph);
                } else {
                    div.textContent = item.subject;
                }
                resultContainer.appendChild(div);
            }
        } else {
            const div = document.createElement("div");
            div.className = "grid-item";
            div.textContent = data.message;
            resultContainer.appendChild(div);
        }
    })
    .catch(error => {
        console.error("An error occurred:", error);
    });
});
