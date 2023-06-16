function toggleIngredient(element) {
    element.classList.toggle("selected");
  }

function handleFileSelect(event) {
  const fileInput = event.target;
  const fileName = fileInput.files[0].name;
  const fileNameElement = fileInput.parentNode.querySelector('.file-name');
  fileNameElement.textContent = fileName;
}