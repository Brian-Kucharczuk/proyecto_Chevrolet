


// VARIABLES//
var menu = document.querySelector('#hamburger-menu .hamburger-list');
var overlay = document.querySelector('#overlay');

/*abrir el menu hamburgesa */
document.getElementById('hamburger-button').addEventListener('click', function() {
    menu.classList.toggle('open');
    overlay.style.display = 'block'; // Muestra el overlay cuando se abre el menú
});

/*cerrar el menu hamburgesa*/
document.getElementById('close-button').addEventListener('click', function() {
    menu.classList.remove('open');
    overlay.style.display = 'none'; // Oculta el overlay cuando se cierra el menú
});

/*Función para cambiar la imagen del auto y mostrar la información del auto*/

var cars = {
    'SUVs': {
        title: 'NEW 2024',
        model: 'Traverse',
        description: 'Between road trips, class trips and whatever adventures pop up along the way, your family is going places. With available seating for up to eight,† best-in-class cargo space† and a suite of innovative tech and safety† features, the New 2024 Traverse has everything you need to keep everyone moving in the right direction.'
    },
    
    'Trucks': {
        title: 'NEW 2024',
        model: 'Silverado 1500',
        description: 'The New 2024 Silverado 1500 is as smart as it is strong, offering technology to keep you connected like available 4G LTE Wi-Fi† and Chevrolet MyLink† with a 7- or 8-inch diagonal color touch-screen display.'
    },

    'Cars': {
        title: 'NEW 2024',
        model: 'Spark',
        description: 'The New 2024 Spark is a small car that’s easy to drive, park and live with. It’s nimble, offers plenty of space for passengers and cargo and has all the safety features you might need.'
    },

    'Electric': {
        title: 'NEW 2024',
        model: 'Bolt EV',
        description: 'The New 2024 Bolt EV is the first affordable all-electric car to offer an EPA-estimated 259 miles of range on a single charge.† It has a long list of impressive characteristics, including some of the most technologically advanced features, stand-out looks and plenty of usable cabin space.'
    },

    'Performance': {
        title: 'NEW 2024',
        model: 'Corvette',
        description: 'The New 2024 Corvette is the first model of the eighth generation of the Corvette sports car, serving as the brand’s halo vehicle and ultimate expression of performance.'
    }
};
    //creo la funcion generatecarhtml//
function generateCarHTML(car) {
    return `
        <h4>${car.title}</h4>
        <h4>${car.model}</h4>
        <p>${car.description}</p>
        <div class="buttons">
            <button>Buy</button>
            <button>Learn More</button>
        </div>
    `;
}
    //creo la funcion changeImage//
function changeImage(src, carType) {
    document.getElementById('carImage').src = src;
    document.getElementById('carText').innerHTML = generateCarHTML(cars[carType]);
}
    //creo la funcion para que el texto de una de las secciones ya aparezca presionado por defecto//
    //llama a la función changeImage cuando la página se carga
window.onload = function() {
    changeImage('img/chevrolet-traverse.avif','SUVs');
};


//seccion baja su opacidad cuando bajas el scroll//
window.addEventListener('scroll', function() {
    var section = document.querySelector('.inicio-container');
    var topOfSection = section.offsetTop;
    var heightOfSection = section.offsetHeight;
    var scrollPosition = window.scrollY;

    if (scrollPosition <= topOfSection + heightOfSection) {
        section.style.opacity = 1 - 0.5 * (scrollPosition - topOfSection) / heightOfSection; // Multiplica por 0.5 para reducir la velocidad de desvanecimiento
    } else {
        section.style.opacity = 0;
    }
});

