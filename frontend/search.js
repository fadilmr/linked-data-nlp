document.getElementById("submitButton").addEventListener("click", function () {
    const queryInput = document.getElementById("queryInput").value;

    fetch("https://backendldt-1-u0544185.deta.app/execute-query", {
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
                const card = document.createElement("div");
                card.className = "bg-white p-5 shadow-md rounded-md hover:bg-gray-100";
                
                if (item.object) {
                    const subjectLink = document.createElement("a");
                    subjectLink.href = `individualDetails.html?individual=${encodeURIComponent(item.subject)}`;
                    subjectLink.textContent = item.subject;
                    subjectLink.className = "hover:text-blue-500";

                    const objectParagraph = document.createElement("p");
                    objectParagraph.textContent = item.object;

                    card.appendChild(subjectLink);
                    card.appendChild(objectParagraph);
                } else {
                    card.textContent = item.subject;
                }
                resultContainer.appendChild(card);
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