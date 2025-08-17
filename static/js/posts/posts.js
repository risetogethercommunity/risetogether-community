// Get elements
const attachmentType = document.getElementById("id_attachment_type");
const imageField = document.getElementById("imageField");
const videoField = document.getElementById("videoField");
const codeField = document.getElementById("codeField");

function toggleFields() {
    const selected = attachmentType.value;

    imageField.classList.add("hidden");
    videoField.classList.add("hidden");
    codeField.classList.add("hidden");

    if (selected === "image") {
        imageField.classList.remove("hidden");
    } else if (selected === "video") {
        videoField.classList.remove("hidden");
    } else if (selected === "code") {
        codeField.classList.remove("hidden");
    }
}

// Run once on page load
toggleFields();

// Run whenever user changes attachment type
if (attachmentType) {
    attachmentType.addEventListener("change", toggleFields);
}
