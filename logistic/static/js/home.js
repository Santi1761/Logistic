const body = document.querySelector('body');
const sidebar = body.querySelector('nav');
const toogle = body.querySelector(".toggle");
const menuItems = body.querySelector(".menu-items");
const modeSwitch = body.querySelector(".toggle-switch");
const modeText = body.querySelector(".mode-text");

toogle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    menuItems.classList.toggle("open");
})

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");
    modeSwitch.classList.toggle("active");
    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode"
    } else {
        modeText.innerText = "Dark mode"
    }
})


const searchInput = document.querySelector('#search-input');
searchInput.addEventListener('keypress', function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        filterTable();
    }
});

function filterTable() {
    const searchInput = document.querySelector('#search-input');
    const searchQuery = searchInput.value.toLowerCase();
    const tableRows = document.querySelectorAll('table tbody tr');

    tableRows.forEach(function (row) {
        const rowText = row.textContent.toLowerCase();
        if (rowText.includes(searchQuery)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(function (progressBar) {
        const progressValue = parseInt(progressBar.textContent);
        progressBar.style.width = progressValue + '%';

        // Asignar clases según el rango de progreso
        if (progressValue >= 0 && progressValue <= 20) {
            progressBar.classList.add('low');
        } else if (progressValue >= 21 && progressValue <= 40) {
            progressBar.classList.add('medium');
        } else if (progressValue >= 41 && progressValue <= 60) {
            progressBar.classList.add('medium-dark');
        } else if (progressValue >= 61 && progressValue <= 80) {
            progressBar.classList.add('high');
        } else if (progressValue >= 81 && progressValue <= 100) {
            progressBar.classList.add('complete');
        }

        // Ocultar el botón de crear tarea si el progreso no es 100%
        if (progressValue !== 100) {
            const createTaskButton = progressBar.closest('tr').querySelector('.new-task');
            if (createTaskButton) {
                createTaskButton.style.display = 'none';
            }
        }
    });
});



// Función para la barra de progreso dinámica
function move() {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(function (progressBar) {
        let width = parseInt(progressBar.textContent);
        let id = setInterval(frame, 10);

        function frame() {
            if (width >= 100) {
                clearInterval(id);
            } else {
                width++;
                progressBar.style.width = width + '%';
            }
        }
    });
}


// Verificar si el modo oscuro está guardado en el almacenamiento local
const darkMode = localStorage.getItem('darkMode');
if (darkMode === 'true') {
    body.classList.add('dark');
    modeSwitch.classList.add('active');
    modeText.innerText = "Modo claro";
}
