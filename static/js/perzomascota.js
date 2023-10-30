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


const Inpts = {
    'tipo':document.querySelector('input#tipo'),
    'estado':document.querySelector('input#estado')
}
const H2s = {
    'tipo':document.querySelector('h2#tipoH2'),
    'estado':document.querySelector('h2#estadoH2')
}
const Botones = document.querySelectorAll('button.listen');
Botones.forEach((el) => {
    el.addEventListener('click', (ev) => {
        const [ side, field ] = ev.target.id.split('-');
        const datalist = Array.from(document.querySelector(`datalist#${field}s`).children).map((ele) => ele.value);
        const actual = datalist.indexOf(H2s[field].innerHTML);
        const newIdx = side === 'R'
            ? actual < datalist.length - 1
                ? actual + 1
                : 0
            : actual - 1;
        Inpts[field].value = datalist[newIdx];
        H2s[field].innerHTML = datalist[newIdx];
    });
});