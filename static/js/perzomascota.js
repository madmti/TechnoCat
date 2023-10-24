const button = document.querySelector('button.edit');
const img = document.querySelector('img.res');
const h1 = document.querySelector('h1#petnameH1');
const input = document.querySelector('input#petname');
const body = document.querySelector('body');

button.addEventListener('click', (e) => {
    e.target.id = e.target.id === 'on'?'':'on';
    if(e.target.id === 'on'){
        img.src = '/static/img/cancelIcon.png';
        h1.classList = 'off';
        input.className = '';
    } else {
        img.src = '/static/img/editIcon.png';
        h1.classList = '';
        input.className = 'off';
    };
});

document.addEventListener('submit', (e) => {
    e.preventDefault();
    body.className = 'gb';
    setTimeout(() => {
        e.target.submit();
    }, 1000);
});

const inptTipo = document.querySelector('input#tipo');
const inptEstado = document.querySelector('input#estado');
const h2Tipo = document.querySelector('h2#tipoH2');
const h2Estado = document.querySelector('h2#estadoH2');
