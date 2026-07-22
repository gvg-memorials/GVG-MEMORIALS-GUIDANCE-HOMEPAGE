(function () {
  const viewer = document.querySelector(".memorial-viewer");
  if (!viewer) return;

  const image = viewer.querySelector(".memorial-viewer-image");
  const label = viewer.querySelector(".memorial-viewer-label");
  const title = viewer.querySelector("#memorial-viewer-title");
  const count = viewer.querySelector(".memorial-viewer-count");
  const closeButton = viewer.querySelector(".memorial-viewer-close");
  const previousButton = viewer.querySelector(".memorial-viewer-prev");
  const nextButton = viewer.querySelector(".memorial-viewer-next");
  const triggers = Array.from(document.querySelectorAll(".completed-card-trigger"));
  let activeIndex = -1;
  let previouslyFocused = null;

  const closeViewer = () => viewer.close();

  const showImage = (index, navigation) => {
    const trigger = triggers[index];
    if (!trigger) return;

    const card = trigger.closest(".completed-card");
    const thumbnail = trigger.querySelector("img");
    const cardLabel = card.querySelector("figcaption span");
    const cardTitle = card.querySelector("figcaption strong");

    activeIndex = index;
    image.src = trigger.href;
    image.alt = thumbnail.alt;
    label.textContent = cardLabel.textContent;
    title.textContent = cardTitle.textContent;
    count.textContent = `${index + 1} of ${triggers.length}`;
    previousButton.disabled = index === 0;
    nextButton.disabled = index === triggers.length - 1;

    if (navigation) {
      window.dispatchEvent(new CustomEvent("gvg:gallery-navigate", {
        detail: {
          category: cardLabel.textContent,
          item: cardTitle.textContent,
          navigation,
        },
      }));
    }
  };

  triggers.forEach((trigger, index) => {
    trigger.addEventListener("click", (event) => {
      if (typeof viewer.showModal !== "function") return;

      event.preventDefault();
      previouslyFocused = trigger;
      showImage(index);
      viewer.showModal();
      document.body.classList.add("memorial-viewer-open");
      closeButton.focus({ preventScroll: true });
    });
  });

  previousButton.addEventListener("click", () => showImage(activeIndex - 1, "previous"));
  nextButton.addEventListener("click", () => showImage(activeIndex + 1, "next"));
  closeButton.addEventListener("click", closeViewer);
  viewer.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      closeViewer();
    } else if (event.key === "ArrowLeft" && !previousButton.disabled) {
      event.preventDefault();
      showImage(activeIndex - 1, "previous");
    } else if (event.key === "ArrowRight" && !nextButton.disabled) {
      event.preventDefault();
      showImage(activeIndex + 1, "next");
    }
  });
  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) closeViewer();
  });
  viewer.addEventListener("close", () => {
    document.body.classList.remove("memorial-viewer-open");
    image.removeAttribute("src");
    activeIndex = -1;
    previouslyFocused?.focus({ preventScroll: true });
    previouslyFocused = null;
  });
})();
