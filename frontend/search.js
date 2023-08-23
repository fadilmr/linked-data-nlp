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
            const gridContainer = document.createElement("div");
            gridContainer.className = "grid grid-cols-2 gap-4";
            
            for (const item of data.data) {
                const card = document.createElement("div");
                card.className = "bg-white p-5 shadow-md rounded-md hover:bg-gray-100";
                
                if (item.object) {
                    const subjectLink = document.createElement("a");
                    subjectLink.href = `details.html?title=${encodeURIComponent(item.subject)}`;
                    subjectLink.textContent = item.subject;
                    subjectLink.className = "hover:text-blue-500";

                    const objectParagraph = document.createElement("p");
                    objectParagraph.textContent = item.object;

                    card.appendChild(subjectLink);
                    card.appendChild(objectParagraph);
                } else {
                    card.textContent = item.subject;
                }
                gridContainer.appendChild(card);
            }
            
            resultContainer.appendChild(gridContainer);
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





