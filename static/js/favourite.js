// ==========================================
// MyCarMarket
// Version: v1.3.0
// File: static/js/favourite.js
// AJAX Favourite Form Submit
// ==========================================

document.addEventListener('DOMContentLoaded', function () {

    const forms = document.querySelectorAll('.ajax-favourite-form');

    forms.forEach(function (form) {

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            event.stopPropagation();

            const button = form.querySelector('.favourite-btn');
            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {

                if (data.success) {

                    if (data.is_favourited) {
                        button.classList.add('saved');
                        button.innerHTML = '❤️';
                    } else {
                        button.classList.remove('saved');
                        button.innerHTML = '🤍';
                    }

                }

            })
            .catch(function (error) {
                console.log('Favourite AJAX error:', error);
            });

        });

    });

});