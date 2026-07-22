(function () {
  const referenceFile = document.querySelector('input[name="reference_file"]');
  const help = document.querySelector("[data-file-help]");
  if (!referenceFile || !help) return;

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
})();
