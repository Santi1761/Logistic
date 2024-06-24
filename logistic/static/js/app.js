document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.querySelector('.menu_button');
    const menu = document.querySelector('.menu');

    let isMenuOpen = false;

    menuButton.addEventListener('click', () => {
        isMenuOpen = !isMenuOpen;

        if (isMenuOpen) {
            menu.style.maxHeight = menu.scrollHeight + "px";
            menu.classList.add('active');
        } else {
            menu.style.maxHeight = null;
            menu.classList.remove('active');
        }
    });
});
