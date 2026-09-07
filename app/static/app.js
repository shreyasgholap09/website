const wishList = document.querySelector("#wish-list");
const wishForm = document.querySelector("#wish-form");
const formStatus = document.querySelector("#form-status");

function renderWishes(wishes) {
  wishList.innerHTML = wishes.map((wish) => `
    <article class="wish-card">
      <p>${escapeHtml(wish.message)}</p>
      <small>from ${escapeHtml(wish.name)}</small>
    </article>
  `).join("");
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

async function loadWishes() {
  try {
    const response = await fetch("/api/wishes");
    renderWishes(await response.json());
  } catch {
    renderWishes([{ name: "the universe", message: "You make the world more interesting just by being in it." }]);
  }
}

wishForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = wishForm.querySelector("button");
  button.disabled = true;
  formStatus.textContent = "pinning your wish...";
  const payload = Object.fromEntries(new FormData(wishForm));

  try {
    const response = await fetch("/api/wishes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Wish book unavailable");
    const newWish = await response.json();
    const current = [...wishList.querySelectorAll(".wish-card")].map((card) => ({
      message: card.querySelector("p").textContent,
      name: card.querySelector("small").textContent.replace("from ", "")
    }));
    renderWishes([newWish, ...current]);
    wishForm.reset();
    formStatus.textContent = "your wish is on the wall ♡";
  } catch {
    formStatus.textContent = "the wish book is shy. Try again in a second.";
  } finally {
    button.disabled = false;
  }
});

loadWishes();
