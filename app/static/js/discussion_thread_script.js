document.addEventListener("DOMContentLoaded", function () {

    const threadRoot = document.getElementById("thread-root");

    const DISCUSSION_ID =
        threadRoot.dataset.discussionId;

    const CURRENT_USER =
        threadRoot.dataset.currentUser;


    // =======================
    // CSRF TOKEN
    // Read from <meta name="csrf-token"> in the page head.
    // Flask-WTF checks this header on all POST requests.
    // =======================

    const CSRF_TOKEN =
        document.querySelector('meta[name="csrf-token"]').content;


    // =======================
    // THREAD REPLY COUNT
    // =======================

    function incrementThreadReplyCount() {

        const countElement =
            document.querySelector(".thread-reply-count");

        if (!countElement) return;

        countElement.textContent =
            parseInt(countElement.textContent) + 1;
    }


    // =======================
    // RELATIVE TIME
    // =======================

    function updateRelativeTime() {

        const times =
            document.querySelectorAll("time.relative-time");

        const now = Date.now();

        times.forEach(time => {

            const datetime =
                time.getAttribute("datetime");

            const created =
                new Date(datetime).getTime();

            const diff =
                Math.floor((now - created) / 1000);

            if (diff < 10) {

                time.innerText = "Just now";

            } else if (diff < 60) {

                time.innerText =
                    `${diff} seconds ago`;

            } else if (diff < 3600) {

                time.innerText =
                    `${Math.floor(diff / 60)} minutes ago`;

            } else if (diff < 86400) {

                time.innerText =
                    `${Math.floor(diff / 3600)} hours ago`;

            } else if (diff < 172800) {

                time.innerText =
                    `${1} day ago`;
            } else {

                time.innerText =
                    `${Math.floor(diff / 86400)} days ago`;
            }

        });

    }

    updateRelativeTime();

    setInterval(updateRelativeTime, 60000);


    // =======================
    // SHOW INLINE ALERT
    // Inserts a Bootstrap alert above the comment box,
    // matching the flash message style in the template.
    // =======================

    function showAlert(message, category = "error") {
        const alertClass = category === "error" ? "danger" : category;

        const alert = document.createElement("div");
        alert.className = `alert alert-${alertClass} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert above the comment box, after any existing alerts
        const commentBox = document.querySelector(".card.p-3.mt-4");
        commentBox.parentElement.insertBefore(alert, commentBox);

        // Auto-dismiss after 4 seconds
        setTimeout(() => alert.remove(), 4000);
    }


    // =======================
    // POST TOP-LEVEL COMMENT
    // =======================

    document.getElementById("post-comment-btn")
        .addEventListener("click", function () {

        const input = document.getElementById("new-comment");
        const text = input.value.trim();

        if (!text) return;

        fetch("/add_comment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({
                discussion_id: DISCUSSION_ID,
                content: text,
                parent_id: null
            })
        })
        .then(res => {
            if (res.status === 401) {
                showAlert("You must be logged in to post a comment.");
                return null;
            }
            return res.json();
        })
        .then(data => {
            if (!data) return;
            document.querySelector(".comments-section")
                .insertAdjacentHTML("beforeend", data.html);
            input.value = "";
            updateRelativeTime();
            incrementThreadReplyCount();
        });
    });


    // =======================
    // GLOBAL CLICK HANDLER
    // =======================

    document.addEventListener("click", function (e) {

        // =======================
        // REPLY BUTTON
        // =======================

        if (e.target.classList.contains("reply-btn")) {
            e.stopPropagation();
            const parent = e.target.closest(".comment");

            // AUTO-EXPAND REPLIES IF COLLAPSED
            const replies = parent.querySelector(".replies");
            const toggleBtn = parent.querySelector(".toggle-replies-btn");

            if (replies && replies.classList.contains("hidden")) {
                replies.classList.remove("hidden");
                if (toggleBtn) {toggleBtn.classList.add("expanded");}
            }
            const existing = parent.querySelector(".reply-box");

            // REMOVE ALL OTHER REPLY BOXES
            document.querySelectorAll(".reply-box").forEach(box => {
                const button = box.parentElement.querySelector(".reply-btn");
                if (button) {button.textContent = "Reply";}
                box.remove();
            });

            // TOGGLE CURRENT BOX OFF
            if (existing) {
                e.target.textContent = "Reply";
                return;
            }

            // CREATE NEW REPLY BOX
            const box = document.createElement("div");
            box.classList.add("reply-box");

            box.innerHTML = `
                <textarea class="form-control mt-2 mb-2"></textarea>
                <button class="btn btn-sm btn-primary submit-reply">
                    Reply
                </button>
            `;

            const repliesContainer = parent.querySelector(".replies");
            if (repliesContainer) {parent.insertBefore(box, repliesContainer);}
            else {parent.appendChild(box);}
            e.target.textContent = "Cancel";
            box.style.opacity = 0;
            setTimeout(() => {
                box.style.opacity = 1;
            }, 10);
        }

        // =======================
        // SUBMIT REPLY
        // =======================

        if (e.target.classList.contains("submit-reply")) {
            const parent = e.target.closest(".comment");
            const parentId = parent.dataset.commentId;
            const replyBox = e.target.closest(".reply-box");
            const text = replyBox.querySelector("textarea").value.trim();

            if (!text) return;

            fetch("/add_comment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN
                },
                body: JSON.stringify({
                    discussion_id: DISCUSSION_ID,
                    content: text,
                    parent_id: parentId
                })
            })

            .then(res => {
                if (res.status === 401) {
                    showAlert("You must be logged in to post a reply.");
                    replyBox.remove();
                    const replyButton = parent.querySelector(".reply-btn");
                    if (replyButton) { replyButton.textContent = "Reply"; }
                    return null;
                }
                return res.json();
            })

            .then(data => {
                if (!data) return;
                let replies = parent.querySelector(".replies");

                // CREATE REPLIES CONTAINER
                if (!replies) {
                    replies = document.createElement("div");
                    replies.classList.add("replies");
                    parent.appendChild(replies);
                }

                // INSERT NEW REPLY
                replies.insertAdjacentHTML("beforeend", data.html);

                // CREATE TOGGLE BUTTON IF FIRST REPLY
                const actions = parent.querySelector(".comment-actions");
                let toggleBtn = parent.querySelector(".toggle-replies-btn");
                if (!toggleBtn) {
                    toggleBtn = document.createElement("button");
                    toggleBtn.classList.add("toggle-replies-btn");
                    toggleBtn.innerHTML = `
                        <span class="reply-arrow">
                            ▶
                        </span>
                        <span class="reply-count">
                            1 reply
                        </span>
                    `;
                    actions.appendChild(toggleBtn);
                }

                // UPDATE REPLY COUNT
                const count = parent.querySelectorAll(".replies .comment").length;
                toggleBtn.querySelector(".reply-count").textContent =
                    count === 1
                        ? "1 reply"
                        : `${count} replies`;

                // REMOVE REPLY BOX
                replyBox.remove();
                const replyButton =
                    parent.querySelector(".reply-btn");
                if (replyButton) {
                    replyButton.textContent = "Reply";
                }
                updateRelativeTime();
                incrementThreadReplyCount();

            });

        }

        // =======================
        // TOGGLE REPLIES
        // =======================

        if (e.target.closest(".toggle-replies-btn")) {

            const button =
                e.target.closest(".toggle-replies-btn");

            const replies =
                button.closest(".comment")
                    .querySelector(".replies");

            if (!replies) return;

            replies.classList.toggle("hidden");

            button.classList.toggle("expanded");
        }

    });
});