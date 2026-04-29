const button = document.getElementById("upload-btn");
const fileInput = document.getElementById("pdf-upload");
const fileNameText = document.getElementById("file-name");

const dropArea = document.getElementById("drop-area");

const pdfPreview = document.getElementById("pdf-preview");
const pdfName = document.getElementById("pdf-name");
const pdfLink = document.getElementById("pdf-link");

let currentURL;

/* NAV TOGGLE */
document.querySelector(".menu-toggle").addEventListener("click", () => {
    document.querySelector(".nav-links").classList.toggle("active");
});

/* upload button */
button.addEventListener("click", () => {
    fileInput.click();
});

/* show pdf */
function showPDF(file) {

    if (currentURL) URL.revokeObjectURL(currentURL);

    currentURL = URL.createObjectURL(file);

    pdfName.textContent = file.name;
    pdfLink.href = currentURL;

    pdfPreview.style.display = "block";
}

/* file input */
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (file && file.type === "application/pdf") {
        showPDF(file);
        fileNameText.textContent = "";
    } else {
        fileNameText.textContent = "Only PDF allowed";
    }
});

/* drag & drop */
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("hover");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("hover");

    const file = e.dataTransfer.files[0];

    if (file && file.type === "application/pdf") {
        showPDF(file);
    }
});