/** like button section */
const toggleContainer = document.querySelector('.toggle-container');
const blogId = toggleContainer.getAttribute('data-blog-id');
const likeBtn = toggleContainer.querySelector('.toggle-btn.like');
const dislikeBtn = toggleContainer.querySelector('.toggle-btn.dislike');

likesData.forEach(entry => {
  if (entry.blog_id == blogId) {
    if (entry.likes) {
      likeBtn.classList.add('activate');
    } else {
      dislikeBtn.classList.add('activate');
    }
  }
});