window.sr = ScrollReveal();
sr.reveal('.navlogo', {
    delay: 110,
    duration: 1900,
    origin: 'bottom',
    distance: '-100px'
});

sr.reveal('nav', {
    delay: 100,
    duration: 1900,
    // origin: 'bottom',
    // distance: '-100px',
});
sr.reveal('footer', {
    duration: 1500,
    origin: 'top',
    distance: '-200px'
});

sr.reveal('.cars-tab', {
    delay: 100,
    duration: 2000,
    // origin: 'bottom',
    // distance: '50px',
    opacity: 0,
    scale: 0.85
});

sr.reveal('.vermas-overlay', { 
    opacity: 0,
    delay: 2500,
    distance: '900px',
    scale: 0.90,
    duration: 1000
});

sr.reveal('.texto-inicio', {
    duration: 2000,
    delay: 70
});

sr.reveal('.texto-inicio h2', {
    duration: 2000,
    delay: 1500
});

sr.reveal('.texto-inicio p', {
    duration: 2000,
    delay: 2000
});

