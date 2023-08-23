window.onload = function () {
    fetch("http://localhost:8000/execute-query-class")
        .then(response => response.json())
        .then(data => {
            console.log("Response from backend:", data);

            const resultContainer = document.getElementById("resultContainer");
            resultContainer.innerHTML = "";

            if (data.data) {
                for (const item of data.data) {
                    const card = document.createElement("div");
                    card.className = "bg-white p-4 shadow-md rounded-md hover:bg-gray-100";

                    const title = document.createElement("h2");
                    title.className = "text-lg font-semibold mb-2";
                    const titleLink = document.createElement("a");
                    titleLink.href = `details.html?class=${encodeURIComponent(item.class)}`;
                    titleLink.textContent = item.judul;
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
};
