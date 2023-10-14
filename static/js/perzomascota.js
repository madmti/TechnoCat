const button = document.querySelector('button.edit');
const img = document.querySelector('img.res');
const h1 = document.querySelector('h1#petname');
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
        location.assign('/menu/1234');
    }, 1000);
});