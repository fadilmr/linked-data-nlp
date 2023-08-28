window.onload = function () {
    const resultContainer = document.getElementById("resultContainer");

    // Get the class name from the query parameter
    const className = getParameterByName("class");
    const backButton = document.getElementById("backButton");
    backButton.addEventListener("click", () => {
        window.location.href = "index.html";
    });
    // Fetch the class details using GET method
    fetch(`https://backendldt-1-u0544185.deta.app/execute-query-class-details/${encodeURIComponent(className)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Response from backend:", data);

            if (data.data && data.data.length > 0) {
                const classData = data.data[0];
                console.log("Class data:", classData);
                const detailsContainer = document.createElement("div");
                detailsContainer.className = "bg-white p-4 shadow-md rounded-md";

                const title = document.createElement("h2");
                title.className = "text-lg font-semibold mb-2";
                title.textContent = classData.label;

                const judul = document.createElement("p");
                judul.className = "text-lg font-semibold mb-2";
                judul.textContent = classData.judul;

                const deskripsi = document.createElement("p");
                deskripsi.className = "text-gray-600";
                deskripsi.textContent = classData.deskripsi;

                detailsContainer.appendChild(judul);
                detailsContainer.appendChild(deskripsi);
                if (classData.instances && classData.instances.length > 0) {
                    const instanceList = document.createElement("ul");
                    instanceList.className = "text-gray-600 mt-4 ml-4 list-disc";
                    for (const instance of classData.instances) {
                        const instanceItem = document.createElement("li");
                        const instanceLink = document.createElement("a");
                        instanceLink.href = `individualDetails.html?individual=${instance}`;
                        instanceLink.textContent = instance;
                        instanceItem.appendChild(instanceLink);
                        instanceList.appendChild(instanceItem);
                    }
                    detailsContainer.appendChild(instanceList);
                }

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