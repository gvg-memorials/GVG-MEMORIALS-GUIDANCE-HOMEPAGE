(function () {
  const viewer = document.querySelector(".memorial-viewer");
  if (!viewer) return;

  const image = viewer.querySelector(".memorial-viewer-image");
  const label = viewer.querySelector(".memorial-viewer-label");
  const title = viewer.querySelector("#memorial-viewer-title");
  const closeButton = viewer.querySelector(".memorial-viewer-close");
  const triggers = document.querySelectorAll(".completed-card-trigger");

  const closeViewer = () => viewer.close();

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      const card = trigger.closest(".completed-card");
      const thumbnail = trigger.querySelector("img");
      const cardLabel = card.querySelector("figcaption span");
      const cardTitle = card.querySelector("figcaption strong");

      if (typeof viewer.showModal !== "function") return;

      event.preventDefault();
      image.src = trigger.href;
      image.alt = thumbnail.alt;
      label.textContent = cardLabel.textContent;
      title.textContent = cardTitle.textContent;
      viewer.showModal();
      document.body.classList.add("memorial-viewer-open");
      closeButton.focus({ preventScroll: true });
    });
  });

  closeButton.addEventListener("click", closeViewer);
  viewer.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    event.preventDefault();
    closeViewer();
  });
  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) closeViewer();
  });
  viewer.addEventListener("close", () => {
    document.body.classList.remove("memorial-viewer-open");
    image.removeAttribute("src");
  });
})();
