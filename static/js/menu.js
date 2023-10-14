const keepCreds = async () => {
    const res = await confirm('Quieres mantener tu sesion iniciada?');
    const cred = location.pathname.substring(6);
    res?window.localStorage.setItem('creds', cred):0;
};

window.localStorage.getItem('creds')?0:keepCreds();

