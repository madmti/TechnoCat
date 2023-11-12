const button = document.querySelector('button.edit');
const img = document.querySelector('img.res');
const h1 = document.querySelector('h1#petnameH1');
const input = document.querySelector('input#petname');
const body = document.querySelector('body');
const iconSpan = document.querySelector('span#icon');

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
const TRAD = {
    'negro':'black',
    'mix_negro':'black-multi',
    'blanco_y_negro':'black-white',
    'gris':'gray',
    'gris_persa':'gray-faded',
    'mix_gris':'gray-multi',
    'gris_tigre':'gray-tiger',
    'gris_y_blanco':'gray-white',
    'naranjo':'orange',
    'naranjo_tigre':'orange-tiger',
    'naranjo_y_blanco':'orange-white',
    'blanco':'white',
    'XL':'xl',
    'pequeño':'small',
    'normal':'regular',
};
Botones.forEach((el) => {
    el.addEventListener('click', (ev) => {
        const [ side, field ] = ev.target.id.split('-');
        const datalist = Array.from(document.querySelector(`datalist#${field}s`).children).map((ele) => ele.value);
        const actual = datalist.indexOf(H2s[field].innerHTML.replace(' ', '_').replace(' ', '_'));
        const newIdx = side === 'R'
            ? actual < datalist.length - 1
                ? actual + 1
                : 0
            : actual > 0 
                ? actual - 1
                :datalist.length - 1;
        Inpts[field].value = datalist[newIdx];
        H2s[field].innerHTML = datalist[newIdx].replace('_', ' ').replace('_', ' ');
        setIconImg();
    });
});
const setIconImg = () => {
    const color = Inpts.estado.value;
    const size = Inpts.tipo.value;
    iconSpan.style.backgroundImage = `url(/static/img/cat/${TRAD[color]}/${TRAD[size]}.png)`;
};
H2s.estado.innerHTML = H2s.estado.innerHTML.replace('_', ' ').replace('_', ' ');