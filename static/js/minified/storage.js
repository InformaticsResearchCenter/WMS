var code = [];


function removeItem(a, id) {
	if (confirm('hapus ga ni ?')) {
		$("#" + id).remove()
		code.splice(code.indexOf(a), 1)
		console.log(code)
	}
}

$(document).ready(function () {


	// var lastResultContainer = '';
	// var lastResult,
	// 	countResults = 0;
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var scanPoint = null;
	var costumer = []
	var items = []
	var html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
		fps: 10,
		qrbox: 250
	});
	html5QrcodeScanner.render(onScanSuccess);
	var pointer, action, itemCode, exist = null;
	var itemlist = JSON.parse($("#itemlist").val())

	function onScanSuccess(qrCodeMessage) {
		if (pointer == "binLocation") {
			$("#binLocation").val("BinLocation - " + qrCodeMessage);
		} else if (pointer == "itemCode") {
			$("#itemCode").val(qrCodeMessage);
		}

	}
	$(".overlay").hide();
	$("#ajaxTesting").click(function (e) {
		e.preventDefault();
		$.ajax({
			type: 'post',
			url: '/storage/testing/',
			data: {
				itemCode: "lol",
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				alert("Success")
			}
		});

	});
	$("#action").change(function (e) {
		e.preventDefault();
		if ($("#action").val() == "move" || $("#action").val() == "inbound") {
			$("#outboundIdContainer").hide();
		} else {
			$("#outboundIdContainer").show();
		}
	});
	$("#binLocation").click(function (e) {
		e.preventDefault();
		pointer = "binLocation"

	});
	$("#itemCode").click(function (e) {
		e.preventDefault();
		pointer = "itemCode"
	});
	$("#outboundId").click(function (e) {
		e.preventDefault();
		pointer = "outboundId"
	});
	$("#inputItem").click(function (e) {
		e.preventDefault();

		for (i = 0; i < itemlist['itembatch'].length; i++) {
			if (itemlist['itembatch'][i].includes($("#itemCode").val())) {
				if (code.includes($("#itemCode").val())) {
					alert("Item telah di scan")
				} else {
					$("#data").append(`<li id="data${i}" onclick="removeItem('${$("#itemCode").val()}','data${i}')">${$("#itemCode").val()}</li>`);
					code.push($("#itemCode").val())
					console.log(code)
				}
				exist = 1;
				break;
			} else {
				exist = null
			}
		}
		if (!exist) {
			alert("Item tidak tersedia")
		}

	});

});