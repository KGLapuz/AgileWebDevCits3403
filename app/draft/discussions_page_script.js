// Discussions list page functions
document.addEventListener("DOMContentLoaded", () => {
    const postBtn = document.getElementById("post-discussion-btn");
    // Only add the listener if the element actually exists on this page
    if (postBtn) {
        document.getElementById("post-discussion-btn").addEventListener("click", function () {
            window.location.href = "create_discussion.html";
        });
    }


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
});
// ---------------------------------------------------------------