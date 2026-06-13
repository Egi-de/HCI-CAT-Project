// Minimal JS; keep empty for now.
console.debug("dashboard UI loaded");

(function () {
  const toggle = document.querySelector('[aria-controls="site-nav"]');
  const items = document.getElementById("site-nav");
  if (!toggle || !items) return;

  toggle.addEventListener("click", () => {
    const isOpen = items.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
})();
