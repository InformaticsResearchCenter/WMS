function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" ||
        document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}
docReady(function () {
    var resultContainer = document.getElementById("code");
    var lastResultContainer = "";
    var button = document.getElementById("button");
    var data = document.getElementById("data");
    var lastResult, countResults = 0;
    var code = [];


    button.addEventListener('click', function () {
        if (resultContainer.value != "" || lastResultContainer != resultContainer.value) {
            code.push(resultContainer.value);
            lastResultContainer = resultContainer.value;
            resultContainer.value = "";
            console.log(code);
            data.value = code;
            console.log("FOOOOOOD")
            console.log("MATTER")
        }

    })

    function onScanSuccess(qrCodeMessage) {
        if (qrCodeMessage !== lastResult) {
            countResults++;
            lastResult = qrCodeMessage;
            resultContainer.value = qrCodeMessage
            //html5QrcodeScanner.clear();
        }
    }

    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", {
            fps: 10,
            qrbox: 250
        });
    html5QrcodeScanner.render(onScanSuccess);
});