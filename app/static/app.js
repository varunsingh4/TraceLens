document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.tab).classList.add("active");
  });
});

function chunkCard(chunk) {
  const filename = chunk.extra_metadata?.filename || chunk.source_name;
  return `<article class="card">
    <div class="meta">
      <span class="score">#${chunk.rank} · ${chunk.score.toFixed(3)}</span>
      <span>${chunk.source_type}</span>
      <span>${filename}</span>
    </div>
    <pre>${escapeHtml(chunk.content)}</pre>
  </article>`;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

document.getElementById("ask-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = document.getElementById("question").value.trim();
  const limit = document.getElementById("limit").value;
  const target = document.getElementById("retrieve-results");
  target.innerHTML = "<p class='lede'>Retrieving…</p>";
  const response = await fetch(`/retrieve?question=${encodeURIComponent(question)}&limit=${limit}`);
  const data = await response.json();
  target.innerHTML = data.results.map(chunkCard).join("") || "<p>No chunks returned.</p>";
});

document.getElementById("eval-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const k = document.getElementById("eval-k").value;
  const target = document.getElementById("eval-results");
  target.innerHTML = "<p class='lede'>Scoring labeled questions…</p>";
  const response = await fetch(`/eval?k=${k}`);
  const data = await response.json();
  const summary = `<article class="card">
    <p class="eyebrow">Mean Recall@${data.k}</p>
    <p class="stat">${data.mean_recall_at_k.toFixed(3)}</p>
  </article>`;
  const rows = data.queries
    .map((query) => {
      const hits = query.hits.map((name) => `<span class="hit">${name}</span>`).join(" · ") || "none";
      const misses = query.misses.map((name) => `<span class="miss">${name}</span>`).join(" · ") || "none";
      return `<article class="card">
        <div class="meta">
          <span class="score">Recall@${query.k} = ${query.recall_at_k.toFixed(3)}</span>
          <span>${query.id}</span>
        </div>
        <p>${escapeHtml(query.question)}</p>
        <p class="meta">Hits: ${hits}</p>
        <p class="meta">Misses: ${misses}</p>
        ${query.chunks.map(chunkCard).join("")}
      </article>`;
    })
    .join("");
  target.innerHTML = summary + rows;
});
