const sendCREDS = (creds) => {
    const form = document.querySelector('form#h');
    const input = document.querySelector('input#creds');
    input.value = creds;
    form.submit();
};
const creds = window.localStorage.getItem('creds');
const href = location.pathname;
href.length > 1 && creds
    ?window.localStorage.removeItem('creds')
    :creds?sendCREDS(creds):0;

const body = document.querySelector('body');
const vars = {
    LogSw:true,
};

document.querySelector('div.container button').addEventListener('click', (e) => {
    const Lform = document.querySelector('div.container form#login');
    const Rform = document.querySelector('div.container form#register');
    if(vars.LogSw){ Lform.className = 'off'; Rform.className = 'on'; vars.LogSw = false; e.target.innerHTML = 'Iniciar secion'; }
    else{ Rform.className = 'off'; Lform.className = 'on'; vars.LogSw = true; e.target.innerHTML = 'Registrarse'; };
});

document.addEventListener('submit', (e) => {
    e.preventDefault();
    body.className = 'gb';
    setTimeout(() => {
        e.target.submit();
    }, 500);
});