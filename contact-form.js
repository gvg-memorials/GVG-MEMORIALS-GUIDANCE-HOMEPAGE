(function () {
  const referenceFile = document.querySelector('input[name="reference_file"]');
  const help = document.querySelector("[data-file-help]");

  if (referenceFile && help) {
    const maxFileSize = 8 * 1024 * 1024;
    const defaultHelp = help.textContent.trim();

    referenceFile.addEventListener("change", () => {
      const file = referenceFile.files?.[0];
      referenceFile.setCustomValidity("");
      help.classList.remove("is-error");
      help.textContent = defaultHelp;

      if (!file || file.size <= maxFileSize) return;

      const message = "Please choose a file smaller than 8 MB.";
      referenceFile.setCustomValidity(message);
      help.classList.add("is-error");
      help.textContent = message;
      referenceFile.reportValidity();
    });
  }

  const contactForm = document.querySelector('form[name="contact"]');
  const submitButton = contactForm?.querySelector('button[type="submit"]');
  if (!contactForm || !submitButton) return;

  const defaultSubmitLabel = submitButton.textContent.trim();
  const resetSubmitButton = () => {
    submitButton.disabled = false;
    submitButton.removeAttribute("aria-busy");
    submitButton.textContent = defaultSubmitLabel;
  };

  contactForm.addEventListener("submit", (event) => {
    if (submitButton.disabled) {
      event.preventDefault();
      return;
    }

    if (!contactForm.checkValidity()) return;

    submitButton.disabled = true;
    submitButton.setAttribute("aria-busy", "true");
    submitButton.textContent = "Sending...";
  });

  window.addEventListener("pageshow", resetSubmitButton);
})();
