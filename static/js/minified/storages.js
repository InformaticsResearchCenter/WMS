function docReady(fn) {
	// see if DOM is already available
	if (document.readyState === 'complete' || document.readyState === 'interactive') {
		// call on next available tick
		setTimeout(fn, 1);
	} else {
		document.addEventListener('DOMContentLoaded', fn);
	}
}
docReady(function () {
	var resultContainer = document.getElementById('code');
	var lastResultContainer = '';
	var button = document.getElementById('button');
	var name = document.getElementById('name');
	var data = document.getElementById('data');
	var lastResult,
		countResults = 0;
	var code = [];

	resultContainer.addEventListener('change', function () {

	})


	button.addEventListener('click', function () {
		var resultValue = resultContainer.value;
		if (data.value.includes(resultValue)) {
			alert("code " + resultValue + " sudah di scan");
		} else {
			code.push(resultValue);
			data.value = code;
			console.log(resultValue.substring(0, 4))

		}
		resultContainer.value = '';
	});

	function onScanSuccess(qrCodeMessage) {
		var item = [{

			"code": "KMJ",
			"name": "kemeja"
		}, {
			"code": "BJP",
			"name": "Baju polos"
		}]
		if (qrCodeMessage !== lastResult) {
			countResults++;
			var resultValue = resultContainer.value;
			var log = null
			for (var i = 0; i < item.length; i++) {
				if (item[i]['code'] === resultValue.substring(0, 3)) {
					name.value = item[i]['name']
					name.classList.add("bounce-top")
					log = 1
					break
				}
			}
			if (log === null) {
				name.value = "item not found"
				name.classList.remove("bounce-top")
			}
		}
		resultContainer.value = qrCodeMessage;

	}


	var html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
		fps: 10,
		qrbox: 250
	});
	html5QrcodeScanner.render(onScanSuccess);
});