function onScanSuccess(decodedText, decodedResult) {
    console.log(`Code scanned = ${decodedText}`, decodedResult);
}
var html5QrcodeScanner = new Html5QrcodeScanner(
	"reader", { fps: 20, qrbox: 250 });

html5QrcodeScanner.render(onScanSuccess, (err) => { console.log(err) });