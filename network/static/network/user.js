document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.edit-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            const postId = button.dataset.id;
            const textarea = document.querySelector(`.edit-textarea[data-id="${postId}"]`);
            const saveButton = document.querySelector(`.save-btn[data-id="${postId}"]`);

            // Toggle visibility of the textarea and save button
            textarea.style.display = 'block';
            saveButton.style.display = 'block';
            button.style.display = 'none';
        });
    });

    document.querySelectorAll('.save-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            const postId = button.dataset.id;
            const textarea = document.querySelector(`.edit-textarea[data-id="${postId}"]`);
            const newContent = textarea.value;

            // Send the updated content to the server
            fetch(`/update_post/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({content: newContent})
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.success) {
                        const postContent = document.querySelector(`.post[data-id="${postId}"] .post-content`);
                        postContent.textContent = newContent;
                        textarea.style.display = 'none';
                        button.style.display = 'none';
                        document.querySelector(`.edit-btn[data-id="${postId}"]`).style.display = 'block';
                    } else {
                        alert('Failed to update the post.');
                    }
                })
                .catch(function (error) {
                    console.error('Error:', error);
                    alert('An error occurred while updating the post.');
                });
        });
    });
});

// Helper function to get CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}