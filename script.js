// Discussions list page functions
document.getElementById("post-discussion-btn").addEventListener("click", function () {
    window.location.href = "create_discussion.html";
});

const searchInput = document.querySelector(".discussion-search input");
const discussions = document.querySelectorAll(".discussion-card");

searchInput.addEventListener("input", function () {
    const query = searchInput.value.toLowerCase();

    discussions.forEach(card => {
        const text = card.innerText.toLowerCase();

        if (text.includes(query)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
});

function openDiscussion() {
    window.location.href = "discussion_thread.html";
}
// ---------------------------------------------------------------

// Create discussions functions
    // Fake save form input
    const form = document.getElementById("create-discussion-form");
    console.log('Form and DOM loaded correctly')
    if (!form) return;

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
    })

    // Cancel button
function goBack() {
    window.location.href = document.referrer;
}
// ---------------------------------------------------------------

