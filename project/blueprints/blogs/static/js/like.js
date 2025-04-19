
document.querySelectorAll('.card').forEach(card => {
    const blogId = card.querySelector('.blog-id').value;
    const likeBtn = card.querySelector('.toggle-btn.like');
    const dislikeBtn = card.querySelector('.toggle-btn.dislike');

    likesData.forEach(entry => {
        if (entry.blog_id == blogId) {
            if (entry.likes) {
                likeBtn.classList.add('activate');
            } else {
                dislikeBtn.classList.add('activate');
            }
        }
     });
});