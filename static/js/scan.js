const inputH = document.querySelector('input#ID');
const form = document.querySelector('form');
const divQr = document.querySelector('div#reader');

function onScanSuccess(decodedText, decodedResult) {
    if (decodedResult.result.format.formatName !== "QR_CODE"){return};
    if (isNaN(decodedText) && isNaN(parseInt(decodedText))){return};

    divQr.className = 'h';
    inputH.value = decodedText;
    form.className = '';
};
var html5QrcodeScanner = new Html5QrcodeScanner(
	"reader", { fps: 20, qrbox: 250 });

html5QrcodeScanner.render(onScanSuccess, (err) => { console.log(err) });
