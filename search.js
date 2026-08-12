// Handles the "Enter a book..." search box: calls the Flask /api/recommend
// endpoint and renders the recommendations returned by recSys.py on the page.

async function loadBookList() {
  try {
    const res = await fetch("/api/books");
    if (!res.ok) return;
    const titles = await res.json();
    const datalist = document.getElementById("bookList");
    if (!datalist) return;
    datalist.innerHTML = titles.map((t) => `<option value="${t}"></option>`).join("");
  } catch (err) {
    console.error("Could not load book list:", err);
  }
}

function renderLoading(container) {
  container.innerHTML = `<p class="results-status">Finding recommendations…</p>`;
}

function renderError(container, message) {
  container.innerHTML = `<p class="results-status results-error">${message}</p>`;
}

function renderSuggestions(container, query, suggestions) {
  if (!suggestions || suggestions.length === 0) {
    renderError(container, `Book "${query}" not found.`);
    return;
  }
  const items = suggestions.map((s) => `<li><button type="button" class="suggestion-btn">${s}</button></li>`).join("");
  container.innerHTML = `
    <p class="results-status">Book "${query}" not found. Did you mean:</p>
    <ul class="suggestion-list">${items}</ul>
  `;

  container.querySelectorAll(".suggestion-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = document.getElementById("bookSearch");
      input.value = btn.textContent;
      runSearch(btn.textContent);
    });
  });
}

function renderRecommendations(container, query, recommendations) {
  if (!recommendations || recommendations.length === 0) {
    renderError(container, `No recommendations found for "${query}".`);
    return;
  }

  const cards = recommendations
    .map(
      (book) => `
      <li class="result-card">
        <h3>${book.title}</h3>
        <p class="result-meta">${book.author}${book.genre ? ` • ${book.genre}` : ""}</p>
      </li>`
    )
    .join("");

  container.innerHTML = `
    <p class="results-status">Because you read "${query}":</p>
    <ul class="result-list">${cards}</ul>
  `;
}

async function runSearch(title) {
  const container = document.getElementById("results");
  if (!container || !title) return;

  renderLoading(container);

  try {
    const res = await fetch(`/api/recommend?title=${encodeURIComponent(title)}`);
    const data = await res.json();

    if (res.ok && data.found) {
      renderRecommendations(container, data.query, data.recommendations);
    } else {
      renderSuggestions(container, data.query ?? title, data.suggestions);
    }
  } catch (err) {
    console.error(err);
    renderError(container, "Something went wrong talking to the server. Is the Flask app running?");
  }
}

function initSearch() {
  const input = document.getElementById("bookSearch");
  const button = document.getElementById("searchBtn");
  if (!input) return;

  loadBookList();

  const trigger = () => runSearch(input.value.trim());

  if (button) button.addEventListener("click", trigger);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") trigger();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSearch);
} else {
  initSearch();
}
