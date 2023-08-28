window.onload = function () {
    const resultContainer = document.getElementById("resultContainer");

    // Get the individual name from the query parameter
    const individualName = getParameterByName("individual");
    const backButton = document.getElementById("backButton");
    backButton.addEventListener("click", () => {
        window.location.href = "index.html";
    });

    // Fetch the individual details using POST method
    fetch("https://backendldt-1-u0544185.deta.app/execute-query-individuals-details", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: individualName })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from backend:", data);

        if (data.data && data.data.length > 0) {
            const individualData = data.data;

            const detailsContainer = document.createElement("div");
            detailsContainer.className = "bg-white p-6 shadow-md rounded-md";

            const title = document.createElement("h2");
            title.className = "text-lg font-semibold mb-2";
            title.textContent = individualName;
            detailsContainer.appendChild(title);
            const deskripsi = document.createElement("p");
            deskripsi.className = "text-gray-600";
            deskripsi.textContent = individualData[0].deskripsi;
            detailsContainer.appendChild(deskripsi);

            const relationList = document.createElement("ul");
            relationList.className = "text-gray-600 mt-4 ml-4 list-disc";

            const relatedIndividualMap = {};

            for (const item of individualData) {
                if (!relatedIndividualMap[item.relation]) {
                    relatedIndividualMap[item.relation] = [];
                }
                relatedIndividualMap[item.relation].push(item.relatedIndividual);
            }

            for (const [relation, relatedIndividuals] of Object.entries(relatedIndividualMap)) {
                const relationItem = document.createElement("li");
                relationItem.textContent = `Relation: ${relation}`;
                const relatedList = document.createElement("ul");

                for (const relatedIndividual of relatedIndividuals) {
                    const relatedItem = document.createElement("li");
                    const relatedLink = document.createElement("a");
                    relatedLink.href = `individualDetails.html?individual=${encodeURIComponent(relatedIndividual)}`;
                    relatedLink.textContent = relatedIndividual;
                    relatedItem.appendChild(relatedLink);
                    relatedList.appendChild(relatedItem);
                }

                relationItem.appendChild(relatedList);
                relationList.appendChild(relationItem);
            }

            detailsContainer.appendChild(relationList);

            resultContainer.appendChild(detailsContainer);
        } else {
            const errorDiv = document.createElement("div");
            errorDiv.className = "text-red-600";
            errorDiv.textContent = "No data available";
            resultContainer.appendChild(errorDiv);
        }
    })
    .catch(error => {
        console.error("An error occurred:", error);
    });
};

// Function to get query parameter by name
function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}