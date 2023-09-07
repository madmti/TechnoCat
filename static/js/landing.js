const vars = {
    LogSw:true,
};

document.querySelector('div.container button').addEventListener('click', (e) => {
    const Lform = document.querySelector('div.container form#login');
    const Rform = document.querySelector('div.container form#register');
    if(vars.LogSw){ Lform.className = 'off'; Rform.className = ''; vars.LogSw = false; e.target.innerHTML = 'Iniciar secion'; }
    else{ Rform.className = 'off'; Lform.className = ''; vars.LogSw = true; e.target.innerHTML = 'Registrarse'; };
});
