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
  const inquiryLink = viewer.querySelector(".memorial-viewer-inquiry");
  const triggers = Array.from(document.querySelectorAll(".completed-card-trigger"));
  let activeIndex = -1;
  let previouslyFocused = null;
  let restoreFocusOnClose = true;
  let pendingInquiryHandoff = false;

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
      restoreFocusOnClose = true;
      showImage(index);
      viewer.showModal();
      document.body.classList.add("memorial-viewer-open");
      closeButton.focus({ preventScroll: true });
    });
  });

  previousButton.addEventListener("click", () => showImage(activeIndex - 1, "previous"));
  nextButton.addEventListener("click", () => showImage(activeIndex + 1, "next"));
  inquiryLink.addEventListener("click", (event) => {
    event.preventDefault();

    const trigger = triggers[activeIndex];
    const card = trigger?.closest(".completed-card");
    const cardLabel = card?.querySelector("figcaption span")?.textContent.trim() || "Completed memorial";
    const cardTitle = card?.querySelector("figcaption strong")?.textContent.trim() || "Similar memorial";
    const contactForm = document.getElementById("contact-form");
    const optionalDetails = contactForm?.querySelector(".contact-form-details");
    const startingPoint = contactForm?.querySelector('select[name="starting_point"]');
    const message = contactForm?.querySelector('textarea[name="message"]');

    if (optionalDetails) optionalDetails.open = true;
    if (startingPoint && !startingPoint.value) startingPoint.value = "Choosing a memorial style";
    if (message && !message.value.trim()) {
      message.value = `I'm interested in a memorial similar to: ${cardTitle}.`;
    }

    window.dispatchEvent(new CustomEvent("gvg:gallery-inquiry", {
      detail: { category: cardLabel, item: cardTitle },
    }));

    restoreFocusOnClose = false;
    pendingInquiryHandoff = true;
    closeViewer();
  });
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
    if (pendingInquiryHandoff) {
      const contactForm = document.getElementById("contact-form");
      const contactFormTitle = document.getElementById("contact-form-title");

      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          const root = document.documentElement;
          const previousScrollBehavior = root.style.scrollBehavior;
          root.style.scrollBehavior = "auto";
          contactForm?.scrollIntoView({ block: "start" });
          window.history.pushState(null, "", "#contact-form");
          window.dispatchEvent(new CustomEvent("gvg:anchor-navigate", {
            detail: { hash: "#contact-form" },
          }));
          contactFormTitle?.focus({ preventScroll: true });
          window.requestAnimationFrame(() => {
            if (previousScrollBehavior) {
              root.style.scrollBehavior = previousScrollBehavior;
            } else {
              root.style.removeProperty("scroll-behavior");
            }
          });
        });
      });
    } else if (restoreFocusOnClose) {
      previouslyFocused?.focus({ preventScroll: true });
    }
    previouslyFocused = null;
    restoreFocusOnClose = true;
    pendingInquiryHandoff = false;
  });
})();
