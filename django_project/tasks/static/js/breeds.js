<script>
        document.addEventListener('DOMContentLoaded', function() {
            // Загрузка текущих голосов при открытии страницы
            document.querySelectorAll('.breed-card').forEach(card => {
                const breedName = card.dataset.breed;
                fetch(`/get_likes/?breed_name=${encodeURIComponent(breedName)}`)
                    .then(response => response.json())
                    .then(data => {
                        card.querySelector('.like-count').textContent = data.likes;
                        card.querySelector('.dislike-count').textContent = data.dislikes;
                    });
            });

            // Обработка кликов по кнопкам
            document.querySelectorAll('.vote-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const card = this.closest('.breed-card');
                    const breedName = card.dataset.breed;
                    const action = this.dataset.action;

                    fetch('/like_breed/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: `breed_name=${encodeURIComponent(breedName)}&action=${action}`
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            // Обновляем счетчики
                            card.querySelector('.like-count').textContent = data.likes;
                            card.querySelector('.dislike-count').textContent = data.dislikes;

                            // Обновляем стили кнопок
                            const likeBtn = card.querySelector('.like-btn');
                            const dislikeBtn = card.querySelector('.dislike-btn');

                            likeBtn.classList.remove('active');
                            dislikeBtn.classList.remove('active');

                            if (data.user_vote === 1) {
                                likeBtn.classList.add('active');
                            } else if (data.user_vote === -1) {
                                dislikeBtn.classList.add('active');
                            }
                        }
                    });
                });
            });

            // Функция для получения CSRF токена
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        });
</script>