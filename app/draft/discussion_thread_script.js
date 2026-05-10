// =======================
// UTIL: RELATIVE TIME
// =======================
function getRelativeTime(timestamp) {
    const now = new Date();
    const diff = Math.floor((now - timestamp) / 1000);

    if (diff < 60) return "just now";
    if (diff < 3600) return Math.floor(diff / 60) + " minutes ago";
    if (diff < 86400) return Math.floor(diff / 3600) + " hours ago";
    return Math.floor(diff / 86400) + " days ago";
}


// =======================
// POST NEW COMMENT
// =======================
const postBtn = document.getElementById("post-comment-btn");

if (postBtn) {
    postBtn.addEventListener("click", function () {
        const input = document.getElementById("new-comment");
        const text = input.value.trim();

        if (!text) return;

        const commentSection = document.querySelector(".comments-section");

        const newComment = document.createElement("div");
        newComment.classList.add("comment");

        newComment.innerHTML = `
            <div class="comment-content">
                <p class="meta">You • ${getRelativeTime(new Date())}</p>
                <p>${text}</p>
                <button class="reply-btn">Reply</button>
            </div>
        `;

        commentSection.appendChild(newComment);
        input.value = "";
    });
}


// =======================
// GLOBAL CLICK HANDLER
// (Reply toggle + collapse)
// =======================
document.addEventListener("click", function (e) {

    // =======================
    // REPLY BUTTON LOGIC
    // =======================
    if (e.target.classList.contains("reply-btn")) {

        e.stopPropagation(); // prevent triggering collapse

        const parentComment = e.target.closest(".comment");
        const existingBox = parentComment.querySelector(".reply-box");

        // 🔴 Close ALL reply boxes + reset buttons
        document.querySelectorAll(".reply-box").forEach(box => {
            const btn = box.parentElement.querySelector(".reply-btn");
            if (btn) btn.textContent = "Reply";
            box.remove();
        });

        // 🟡 If this one was already open → just close
        if (existingBox) {
            e.target.textContent = "Reply";
            return;
        }

        // 🟢 Create reply box
        const replyBox = document.createElement("div");
        replyBox.classList.add("reply-box");

        replyBox.innerHTML = `
            <textarea class="form-control mt-2 mb-2" placeholder="Write a reply..."></textarea>
            <button class="btn btn-sm btn-primary submit-reply">Reply</button>
        `;

        parentComment.appendChild(replyBox);

        // Change button text
        e.target.textContent = "Cancel";

        // Submit reply
        const submitBtn = replyBox.querySelector(".submit-reply");

        submitBtn.addEventListener("click", function () {
            const text = replyBox.querySelector("textarea").value.trim();
            if (!text) return;

            let repliesContainer = parentComment.querySelector(".replies");

            if (!repliesContainer) {
                repliesContainer = document.createElement("div");
                repliesContainer.classList.add("replies");
                parentComment.appendChild(repliesContainer);
            }

            const reply = document.createElement("div");
            reply.classList.add("comment", "reply");

            reply.innerHTML = `
                <div class="comment-content">
                    <p class="meta">You • ${getRelativeTime(new Date())}</p>
                    <p>${text}</p>
                    <button class="reply-btn">Reply</button>
                </div>
            `;

            repliesContainer.appendChild(reply);

            // Cleanup
            replyBox.remove();
            e.target.textContent = "Reply";
        });
    }


    // =======================
    // COLLAPSE / EXPAND THREAD
    // =======================
    const commentContent = e.target.closest(".comment-content");

    // only trigger if NOT clicking buttons or textarea
    if (
        commentContent &&
        !e.target.classList.contains("reply-btn") &&
        !e.target.classList.contains("submit-reply") &&
        e.target.tagName !== "TEXTAREA"
    ) {
        const parentComment = commentContent.closest(".comment");
        const replies = parentComment.querySelector(".replies");

        if (replies) {
            replies.style.display =
                (replies.style.display === "none") ? "block" : "none";
        }
    }
});