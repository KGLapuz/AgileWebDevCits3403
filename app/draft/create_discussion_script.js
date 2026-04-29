// Create discussions functions
    // Fake save form input
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("create-discussion-form");

    if (form) {
        console.log('Form and DOM loaded correctly')

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const title = document.getElementById("title").value.trim();
            const unit = document.getElementById("unit").value;
            const content = document.getElementById("content").value.trim();

            if (!title || !unit || !content) {
                alert("Please fill in all required fields.");
                return;
            }

            alert("Discussion posted successfully!");

            // redirect after short delay (so alert feels smoother)
            setTimeout(() => {
                window.location.href = "discussions_page.html";
            }, 300);
        });
    } else {
        console.error("Form element not found.")
    }
});

    // Cancel button
function goBack() {
    window.location.href = document.referrer;
}
// ---------------------------------------------------------------

