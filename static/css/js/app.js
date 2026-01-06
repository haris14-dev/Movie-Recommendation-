const searchInput = document.getElementById("search");
const suggestionsDiv = document.getElementById("suggestions");
const recDiv = document.getElementById("recommendations");

// Search input event
searchInput.addEventListener("input", async () => {
    const query = searchInput.value;
    if (!query) {
        suggestionsDiv.innerHTML = "";
        return;
    }

    try {
        const res = await fetch(`/api/suggestions/?query=${query}`);
        const data = await res.json();

        suggestionsDiv.innerHTML = "";
        data.suggestions.forEach(movie => {
            const div = document.createElement("div");
            div.textContent = movie;
            div.onclick = () => getRecommendations(movie);
            suggestionsDiv.appendChild(div);
        });
    } catch (err) {
        console.error("Error fetching suggestions:", err);
    }
});

// Fetch recommendations for selected movie
async function getRecommendations(movie) {
    suggestionsDiv.innerHTML = "";
    searchInput.value = movie;

    try {
        const res = await fetch(`/api/recommendations/?movie=${movie}`);
        const data = await res.json();

        recDiv.innerHTML = "<h2>🎯 Recommended Movies</h2>";

        data.recommendations.forEach(m => {
            recDiv.innerHTML += `
                <div class="card">
                    <img src="${m.poster_url}" alt="${m.title}" class="poster">
                    <strong>${m.title}</strong><br>
                    ⭐ Rating: ${m.mean.toFixed(2)}<br>
                    🎟️ Votes: ${m.count}
                </div>
            `;
        });
    } catch (err) {
        console.error("Error fetching recommendations:", err);
    }
}
