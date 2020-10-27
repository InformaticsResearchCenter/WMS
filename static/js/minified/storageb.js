$(document).ready(function () {
	var resultContainer = document.getElementById('code');
	var lastResultContainer = '';
	var button = document.getElementById('button');
	var name = document.getElementById('name');
	var data = document.getElementById('data');
	var lastResult,
		countResults = 0;
	var code = [];
	var itemlist = document.getElementById('itemlist');
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var scanPoint = null;
	var costumer = []
	var items = []
	var html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
		fps: 10,
		qrbox: 250
	});

	$("#inbound").hide();
	$("#outbound").hide();
	$("#move").hide();
	$(".flex-item").hide();
	$("#storageOverlay").hide();
	function onScanSuccess(qrCodeMessage) {
		var itemlist = JSON.parse(document.getElementById('itemlist').value);
		// if (qrCodeMessage !== lastResult) {
		// 	countResults++;
		// 	var resultValue = resultContainer.value;
		// 	var result = resultValue.replace('"', '');
		// 	var result1 = result.replace('"', '');
		// 	var log = null;
		// 	var findId = 0;
		// 	for (var i = 0; i < itemlist['item'].length; i++) {
		// 		findId = result1.search('I');
		// 		console.log();
		// 		if (itemlist['item'][i][0] === result1.substring(findId)) {
		// 			name.value = itemlist['item'][i][1];
		// 			name.classList.add('bounce-top');
		// 			log = 1;
		// 			break;
		// 		}
		// 	}
		// 	if (log === null) {
		// 		name.value = 'item not found';
		// 		name.classList.remove('bounce-top');
		// 	}
		// }
		if(scanPoint == "inboundBinlocation"){
			$("#inboundBinlocation").val(qrCodeMessage);
		}
		else if(scanPoint == "inboundItemCode"){
			$("#inboundItemCode").val(qrCodeMessage);
		}
		if(scanPoint == "moveBinlocation"){
			$("#moveBinlocation").val(qrCodeMessage);
		}
		else if(scanPoint == "moveItemCode"){
			$("#moveItemCode").val(qrCodeMessage);
		}
		if(scanPoint == "outboundId"){
			$("#outboundId").val(qrCodeMessage);
		}
		else if(scanPoint == "outboundItemCode"){
			$("#outboundItemCode").val(qrCodeMessage);
		}
	}
	 


	// input item
	$("#inboundInputButton").click(function (e) { 
		e.preventDefault();
		var scannedCode = $("#inboundItemCode").val();
		if ($("#inboundScannedItem").val().includes(scannedCode)) {
			alert('code ' + scannedCode + ' sudah di scan');
		} else {
			code.push({
				code: scannedCode
			});
			$("#inboundScannedItem").val($("#inboundScannedItem").val()+scannedCode + "\n");
			console.log("scanned item")
			console.log(code)
		}
		// resultContainer.value = '';
		
	});
	$("#outboundInputButton").click(function (e) { 
		e.preventDefault();
		var scannedCode = $("#outboundItemCode").val();
		if ($("#outboundScannedItem").val().includes(scannedCode)) {
			alert('code ' + scannedCode + ' sudah di scan');
		} else {
			code.push({
				code: scannedCode
			});
			$("#outboundScannedItem").val($("#outboundScannedItem").val()+scannedCode + "\n");
			console.log("scanned item")
			console.log(code)
		}
		// resultContainer.value = '';
		
	});
	$("#moveInputButton").click(function (e) { 
		e.preventDefault();
		var scannedCode = $("#moveItemCode").val();
		if ($("#moveScannedItem").val().includes(scannedCode)) {
			alert('code ' + scannedCode + ' sudah di scan');
		} else {
			code.push({
				code: scannedCode
			});
			$("#moveScannedItem").val($("#moveScannedItem").val()+scannedCode + "\n");
			console.log(code)
		}
		// resultContainer.value = '';
		
	});
	
	// Scanner button toggle
	$("#inboundItemCodeButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "inboundItemCode"
		console.log(scanPoint)
		
	});
	$("#inboundBinlocationButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "inboundBinlocation"
		console.log(scanPoint)
		
	});
	$("#outboundItemCodeButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "outboundItemCode"
		console.log(scanPoint)
	});
	$("#moveItemCodeButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "moveItemCode"
		console.log(scanPoint)
		
	});
	$("#moveBinlocationButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "moveBinlocation"
		console.log(scanPoint)
		
	});
	$("#outboundIdButton").click(function (e) { 
		e.preventDefault();
		scanPoint = "outboundId"
		console.log(scanPoint)

	});
 
	$("#opt").change(function (e) {
		console.log($("#opt").val())
		html5QrcodeScanner.render(onScanSuccess);
		$(".flex-item").show();
		if($("#opt").val() == "inbound"){
			$("#cardStorage").text("Storage - Inbound");
			$("#inbound").show();
			$("#outbound").hide();
			$("#move").hide();
		}
		else if($("#opt").val() == "outbound"){
			$("#cardStorage").text("Storage - Outbound");
			$("#inbound").hide();
			$("#outbound").show();
			$("#move").hide();
		}
		else if($("#opt").val() == "move"){
			$("#cardStorage").text("Storage - Move");
			$("#inbound").hide();
			$("#outbound").hide();
			$("#move").show();
		}
	});
	// finish input
	$('#inboundFinish').click(function () {
		console.log(code);
		if (confirm('Sure ?')) {
			alert('ok');
			$.ajax({
				type: 'post',
				url: '/storage/put/',
				data: {
					binlocation: $("#inboundBinlocation").val(),
					itemCode: JSON.stringify(code),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					alert("Success")
				}
			});
			code = [];
			$('#code').val('');
			$('#name').val('');
			$('#data').val('');
		}
	});
	$('#moveFinish').click(function () {
		console.log(code);
		if (confirm('Sure ?')) {
			alert('ok');
			$.ajax({
				type: 'post',
				url: '/storage/move/',
				data: {
					binlocation: $("#moveBinlocation").val(),
					itemCode: JSON.stringify(code),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					alert("Moved")
				}
			});
			code = [];
			$('#code').val('');
			$('#name').val('');
			$('#data').val('');
		}
	});

	$('#outboundIdCheckButton').click(function () {
		console.log(code);
		$("#systeminfo").val("Loading data");
		$("#storageOverlay").show();

			$.ajax({
				type: 'post',
				url: '/storage/checkOutbound/',
				data: {
					outboundId: $("#outboundId").val(),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					costumer = response['costumer']
					items = response['items']
					console.log(costumer)
					console.log(items)
					$("#systeminfo").val("Data Loaded");
					$("#storageOverlay").hide();
				}
			});
	});
	$("#dummy").click(function (e) { 
		e.preventDefault();
		alert(costumer[0])
		alert(items)
		
	});
	// button.addEventListener('click', function () {
	// 	var resultValue = resultContainer.value;
	// 	if (data.value.includes(resultValue)) {
	// 		alert('code ' + resultValue + ' sudah di scan');
	// 	} else {
	// 		code.push({
	// 			code: resultValue
	// 		});
	// 		data.value = code;
	// 		// console.log(code)
	// 	}
	// 	resultContainer.value = '';
	// });

	// --------------------------------------------------------
	// ---------------- Scanner area --------------------------
	// --------------------------------------------------------

	


});

