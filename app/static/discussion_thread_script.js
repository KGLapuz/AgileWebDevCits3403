document.addEventListener("DOMContentLoaded", function () {

    const threadRoot = document.getElementById("thread-root");
    const DISCUSSION_ID = threadRoot.dataset.discussionId;
    const CURRENT_USER = threadRoot.dataset.currentUser;

    // =======================
    // USER SWITCH
    // =======================
    // 👇 choose which user you want
    // optional manual switch for testing only
    window.switchUser = function(id) {
        fetch("/set_user", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ user_id: id })
        }).then(() => location.reload());
    }

    // You can switch user by running switchUser(1) or switchUser(2) in the console. This is just for testing purposes to simulate different users without a full auth system.


    // =======================
    // RELATIVE TIME
    // =======================
    function updateRelativeTime() {
        const times = document.querySelectorAll('time.relative-time');
        const now = new Date();

        times.forEach(time => {
            const date = new Date(time.getAttribute('datetime'));
            const diff = Math.floor((now - date) / 1000);

            if (diff < 60) time.innerText = "Just now";
            else if (diff < 3600) time.innerText = Math.floor(diff/60) + " minutes ago";
            else if (diff < 86400) time.innerText = Math.floor(diff/3600) + " hours ago";
            else time.innerText = Math.floor(diff/86400) + " days ago";
        });
    }

    updateRelativeTime();
    setInterval(updateRelativeTime, 60000); // 🔥 auto refresh


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
            document.querySelector(".comments-section")
                .insertAdjacentHTML("beforeend", data.html);

            input.value = "";
            updateRelativeTime();
        });
    });


    // =======================
    // GLOBAL CLICK HANDLER
    // =======================
    document.addEventListener("click", function (e) {

        // REPLY TOGGLE
        if (e.target.classList.contains("reply-btn")) {

            e.stopPropagation();

            const parent = e.target.closest(".comment");
            const existing = parent.querySelector(".reply-box");

            document.querySelectorAll(".reply-box").forEach(box => {
                box.parentElement.querySelector(".reply-btn").textContent = "Reply";
                box.remove();
            });

            if (existing) {
                e.target.textContent = "Reply";
                return;
            }

            const box = document.createElement("div");
            box.classList.add("reply-box");

            box.innerHTML = `
                <textarea class="form-control mt-2 mb-2"></textarea>
                <button class="btn btn-sm btn-primary submit-reply">Reply</button>
            `;

            parent.appendChild(box);
            e.target.textContent = "Cancel";

            box.style.opacity = 0;
            setTimeout(() => box.style.opacity = 1, 10); // ✨ subtle animation
        }


        // SUBMIT REPLY
        if (e.target.classList.contains("submit-reply")) {

            const parent = e.target.closest(".comment");
            const parentId = parent.dataset.commentId;
            const text = parent.querySelector("textarea").value.trim();

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

                let replies = parent.querySelector(".replies");

                if (!replies) {
                    replies = document.createElement("div");
                    replies.classList.add("replies");
                    parent.appendChild(replies);
                }

                replies.insertAdjacentHTML("beforeend", data.html);

                parent.querySelector(".reply-box").remove();
                parent.querySelector(".reply-btn").textContent = "Reply";

                updateRelativeTime();
            });
        }


        // COLLAPSE THREAD
        const content = e.target.closest(".comment-content");

        if (
            content &&
            !e.target.classList.contains("reply-btn") &&
            !e.target.classList.contains("submit-reply") &&
            e.target.tagName !== "TEXTAREA"
        ) {
            const parent = content.closest(".comment");
            const replies = parent.querySelector(".replies");

            if (replies) {
                replies.style.display =
                    replies.style.display === "none" ? "block" : "none";
            }
        }

    });

});