window.onload = function () {
    const resultContainer = document.getElementById("resultContainer");
    let selectedClass = null; // Variable to store the selected class

    fetch("http://localhost:8000/execute-query-class")
        .then(response => response.json())
        .then(data => {
            console.log("Response from backend:", data);

            if (data.data) {
                for (const item of data.data) {
                    const card = document.createElement("div");
                    card.className = "bg-white p-4 shadow-md rounded-md hover:bg-gray-100";

                    const title = document.createElement("h2");
                    title.className = "text-lg font-semibold mb-2";
                    const titleLink = document.createElement("a");
                    titleLink.href = "#"; // Change to "#" for now, we'll handle the click event later
                    titleLink.textContent = item.judul;
                    titleLink.className = "class-title-link"; // Add a class for identifying the title link
                    title.appendChild(titleLink);

                    const description = document.createElement("p");
                    description.className = "text-gray-600";
                    const maxDescriptionLength = 100;
                    description.textContent = item.deskripsi.length > maxDescriptionLength
                        ? `${item.deskripsi.substring(0, maxDescriptionLength)}...`
                        : item.deskripsi;

                    card.appendChild(title);
                    card.appendChild(description);
                    resultContainer.appendChild(card);

                    // Store the selected class in the variable when the title link is clicked
                    titleLink.addEventListener("click", function() {
                        selectedClass = item.class;
                    });
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

    // Add an event listener to the document for detecting when a title link is clicked
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("class-title-link")) {
            // Trigger the details.js script with the selected class
            const encodedClassName = encodeURIComponent(selectedClass); // Encode the class name
            window.location.href = `details.html?classname=${encodedClassName}`;
        }
    });
};