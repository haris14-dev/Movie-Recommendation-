const searchInput = document.getElementById("search");
const suggestionsDiv = document.getElementById("suggestions");
const recDiv = document.getElementById("recommendations");

searchInput.addEventListener("input", async () => {
    const query = searchInput.value;
    if (!query) {
        suggestionsDiv.innerHTML = "";
        return;
    }

    const res = await fetch(`/api/suggestions/?query=${query}`);
    const data = await res.json();

    suggestionsDiv.innerHTML = "";
    data.suggestions.forEach(movie => {
        const div = document.createElement("div");
        div.textContent = movie;
        div.onclick = () => getRecommendations(movie);
        suggestionsDiv.appendChild(div);
    });
});

async function getRecommendations(movie) {
    suggestionsDiv.innerHTML = "";
    searchInput.value = movie;

    const res = await fetch(`/api/recommendations/?movie=${movie}`);
    const data = await res.json();

    recDiv.innerHTML = "<h2>🎯 Recommended Movies</h2>";
    data.recommendations.forEach(m => {
        recDiv.innerHTML += `
            <div class="card">
                <strong>${m.title}</strong><br>
                ⭐ Rating: ${m.mean.toFixed(2)}<br>
                🎟️ Votes: ${m.count}
            </div>
        `;
    });
}
