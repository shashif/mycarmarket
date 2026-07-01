document.addEventListener('DOMContentLoaded', function () {

    const btn = document.getElementById('scrollTopBtn');

    if (!btn) {
        console.log('Scroll button not found');
        return;
    }

    console.log('Scroll button loaded');

    window.addEventListener('scroll', function () {

        if (window.scrollY > 50) {
            btn.style.display = 'block';
        } else {
            btn.style.display = 'none';
        }

    });

    btn.addEventListener('click', function () {

        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });

    });

});