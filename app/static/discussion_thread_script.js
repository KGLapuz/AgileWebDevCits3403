document.addEventListener("DOMContentLoaded", function () {

    const threadRoot = document.getElementById("thread-root");
    const DISCUSSION_ID = threadRoot.dataset.discussionId;


    // =======================
    // RELATIVE TIME
    // =======================
    function updateRelativeTime() {
        const times = document.querySelectorAll('time.relative-time');
        const now = new Date();

        times.forEach(time => {
            const date = new Date(time.getAttribute('datetime'));
            const diffSeconds = Math.round((now - date) / 1000);

            if (diffSeconds < 60) time.innerText = 'Just now';
            else if (diffSeconds < 3600) time.innerText = Math.floor(diffSeconds / 60) + ' minutes ago';
            else if (diffSeconds < 86400) time.innerText = Math.floor(diffSeconds / 3600) + ' hours ago';
            else time.innerText = Math.floor(diffSeconds / 86400) + ' days ago';
        });
    }

    updateRelativeTime();


    // =======================
    // CREATE COMMENT HTML
    // =======================
    function createCommentHTML(data) {
        return `
            <div class="comment" data-comment-id="${data.comment_id}">
                <div class="comment-content">
                    <p class="meta">
                        ${data.author} • 
                        <time class="relative-time" datetime="${data.created_at}"></time>
                    </p>
                    <p>${data.content}</p>
                    <button class="reply-btn">Reply</button>
                </div>
            </div>
        `;
    }


    // =======================
    // POST COMMENT
    // =======================
    document.getElementById("post-comment-btn").addEventListener("click", function () {

        const input = document.getElementById("new-comment");
        const text = input.value.trim();

        if (!text) return;

        fetch("/add_comment", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                discussion_id: DISCUSSION_ID,
                content: text,
                parent_id: null
            })
        })
        .then(res => res.json())
        .then(data => {

            const section = document.querySelector(".comments-section");

            section.insertAdjacentHTML("beforeend", createCommentHTML(data));

            input.value = "";

            updateRelativeTime(); // 🔥 update new timestamp
        });
    });


    // =======================
    // GLOBAL CLICK HANDLER
    // =======================
    document.addEventListener("click", function (e) {

        // =======================
        // REPLY BUTTON TOGGLE
        // =======================
        if (e.target.classList.contains("reply-btn")) {

            e.stopPropagation();

            const parentComment = e.target.closest(".comment");
            const existingBox = parentComment.querySelector(".reply-box");

            // close all others
            document.querySelectorAll(".reply-box").forEach(box => {
                const btn = box.parentElement.querySelector(".reply-btn");
                if (btn) btn.textContent = "Reply";
                box.remove();
            });

            // toggle off
            if (existingBox) {
                e.target.textContent = "Reply";
                return;
            }

            // create reply box
            const replyBox = document.createElement("div");
            replyBox.classList.add("reply-box");

            replyBox.innerHTML = `
                <textarea class="form-control mt-2 mb-2" placeholder="Write a reply..."></textarea>
                <button class="btn btn-sm btn-primary submit-reply">Reply</button>
            `;

            parentComment.appendChild(replyBox);
            e.target.textContent = "Cancel";
        }


        // =======================
        // SUBMIT REPLY
        // =======================
        if (e.target.classList.contains("submit-reply")) {

            const parentComment = e.target.closest(".comment");
            const parentId = parentComment.dataset.commentId;

            const replyBox = parentComment.querySelector(".reply-box");
            const text = replyBox.querySelector("textarea").value.trim();

            if (!text) return;

            fetch("/add_comment", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    discussion_id: DISCUSSION_ID,
                    content: text,
                    parent_id: parentId
                })
            })
            .then(res => res.json())
            .then(data => {

                let repliesContainer = parentComment.querySelector(".replies");

                if (!repliesContainer) {
                    repliesContainer = document.createElement("div");
                    repliesContainer.classList.add("replies");
                    parentComment.appendChild(repliesContainer);
                }

                repliesContainer.insertAdjacentHTML("beforeend", createCommentHTML(data));

                replyBox.remove();
                parentComment.querySelector(".reply-btn").textContent = "Reply";

                updateRelativeTime(); // 🔥 update time
            });
        }


        // =======================
        // COLLAPSE THREAD
        // =======================
        const commentContent = e.target.closest(".comment-content");

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

});