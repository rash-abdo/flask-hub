const likeBtn = document.getElementById('likeBtn');
const dislikeBtn = document.getElementById('dislikeBtn');

likeBtn.addEventListener('click', () => {
  if (likeBtn.classList.contains('active')) {
    likeBtn.classList.remove('active');
  } else {
    likeBtn.classList.add('active');
    dislikeBtn.classList.remove('active');
  }
});

dislikeBtn.addEventListener('click', () => {
  if (dislikeBtn.classList.contains('active')) {
    dislikeBtn.classList.remove('active');
  } else {
    dislikeBtn.classList.add('active');
    likeBtn.classList.remove('active');
  }
});