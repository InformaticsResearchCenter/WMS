// function docReady(fn) {
// 	// see if DOM is already available
// 	if (document.readyState === 'complete' || document.readyState === 'interactive') {
// 		// call on next available tick
// 		setTimeout(fn, 1);
// 	} else {
// 		document.addEventListener('DOMContentLoaded', fn);
// 	}
// }
$(document).ready(function () {
	var resultContainer = document.getElementById('code');
	var lastResultContainer = '';
	var button = document.getElementById('button');
	var name = document.getElementById('name');
	var data = document.getElementById('data');
	var lastResult,
		countResults = 0;
	var code = [];
	var dodo = document.getElementById('dodo');
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	// resultContainer.addEventListener('change', function () {})
	// dodo.innerHTML += item;
	$('#code').click(function () {
		console.log(code);
		if (confirm("Sure ?")) {
			alert("ok")
		}
		$.ajax({
			type: "post",
			url: "/storage/put/",
			data: {
				codedata: JSON.stringify(code),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {

			}
		});
		code = []
		$('#code').val("");
		$('#name').val("");
		$('#data').val("");

	});
	button.addEventListener('click', function () {
		var resultValue = resultContainer.value;
		if (data.value.includes(resultValue)) {
			alert("code " + resultValue + " sudah di scan");
		} else {
			code.push({
				code: resultValue
			});
			data.value = code;
			// console.log(code)

		}
		resultContainer.value = '';
	});

	// --------------------------------------------------------
	// ---------------- Scanner area --------------------------
	// --------------------------------------------------------

	function onScanSuccess(qrCodeMessage) {
		var itemlist = JSON.parse(document.getElementById('dodo').value)
		if (qrCodeMessage !== lastResult) {
			countResults++;
			var resultValue = resultContainer.value;
			var result = resultValue.replace('"', '')
			var result1 = result.replace('"', '')
			var log = null
			var findId = 0
			for (var i = 0; i < itemlist['item'].length; i++) {
				findId = result1.search("I")
				console.log()
				if (itemlist['item'][i][0] === result1.substring(findId)) {
					name.value = itemlist['item'][i][1]
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

// docReady(function () {
// 	var resultContainer = document.getElementById('code');
// 	var lastResultContainer = '';
// 	var button = document.getElementById('button');
// 	var name = document.getElementById('name');
// 	var data = document.getElementById('data');
// 	var lastResult,
// 		countResults = 0;
// 	var code = [];
// 	var dodo = document.getElementById('dodo');

// 	resultContainer.addEventListener('change', function () {})
// 	dodo.innerHTML += item;
// 	button.addEventListener('click', function () {
// 		var resultValue = resultContainer.value;
// 		if (data.value.includes(resultValue)) {
// 			alert("code " + resultValue + " sudah di scan");
// 		} else {
// 			code.push({
// 				code: resultValue
// 			});
// 			data.value = code;
// 			console.log(code)

// 		}
// 		resultContainer.value = '';
// 	});


// 	function onScanSuccess(qrCodeMessage) {
// 		var itemlist = JSON.parse(document.getElementById('dodo').value)
// 		if (qrCodeMessage !== lastResult) {
// 			countResults++;
// 			var resultValue = resultContainer.value;
// 			var result = resultValue.replace('"', '')
// 			var result1 = result.replace('"', '')
// 			var log = null
// 			var findId = 0
// 			for (var i = 0; i < itemlist['item'].length; i++) {
// 				findId = result1.search("I")
// 				console.log()
// 				if (itemlist['item'][i][0] === result1.substring(findId)) {
// 					name.value = itemlist['item'][i][1]
// 					name.classList.add("bounce-top")
// 					log = 1
// 					break
// 				}
// 			}
// 			if (log === null) {
// 				name.value = "item not found"
// 				name.classList.remove("bounce-top")
// 			}
// 		}
// 		resultContainer.value = qrCodeMessage;
// 	}


// 	var html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
// 		fps: 10,
// 		qrbox: 250
// 	});
// 	html5QrcodeScanner.render(onScanSuccess);
// });