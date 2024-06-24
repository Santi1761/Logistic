document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'America/Bogota',
        initialView: 'dayGridMonth',
        events: eventsJsonData,
        eventContent: function(arg) {
            var adjustedColor = adjustColor(arg.event.backgroundColor, -100);
            
            // Creamos un contenedor para los elementos del evento
            var eventContainer = document.createElement('div');
            eventContainer.style.overflow = 'hidden';
            eventContainer.style.fontSize = '12px';
            eventContainer.style.position = 'relative';
            eventContainer.style.cursor = 'pointer';
            eventContainer.style.fontFamily = "'Inter', sans-serif";

            // Título del evento en negrita
            var titleElement = document.createElement('div');
            titleElement.innerHTML = `<strong>${arg.event.title}</strong>`;
            titleElement.style.color = adjustedColor;
            titleElement.style.fontWeight = 'bold';

            // Usuario del evento
            var userElement = document.createElement('div');
            userElement.textContent = `Usuario: ${arg.event.extendedProps.username}`;
            userElement.style.color = adjustedColor;
            userElement.style.fontWeight = 'bold';

            eventContainer.appendChild(titleElement);
            eventContainer.appendChild(userElement);

            return { domNodes: [eventContainer] };
        },
        eventClick: function(info) {
            // Acciones para cuando se hace clic en un evento, si es necesario
            info.jsEvent.preventDefault();
            if (info.event.url) {
                window.open(info.event.url, "_self");
            }
        },
    });

    calendar.render();
    calendar.setOption('locale', 'es');
});


// Función para ajustar el brillo del color
function adjustColor(color, amount) {
    var usePound = false;

    if (color[0] == "#") {
        color = color.slice(1);
        usePound = true;
    }

    var num = parseInt(color, 16);
    var r = (num >> 16) + amount;
    if (r > 255) r = 255;
    else if (r < 0) r = 0;

    var b = ((num >> 8) & 0x00FF) + amount;
    if (b > 255) b = 255;
    else if (b < 0) b = 0;

    var g = (num & 0x0000FF) + amount;
    if (g > 255) g = 255;
    else if (g < 0) g = 0;

    return (usePound ? "#" : "") + ((r << 16) | (b << 8) | g).toString(16);
}
