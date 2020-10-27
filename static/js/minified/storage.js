$(document).ready(function () {
	var lastResultContainer = '';
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
	html5QrcodeScanner.render(onScanSuccess);
	var pointer, action, itemCode = null

	function onScanSuccess(qrCodeMessage) {
		// var itemlist = JSON.parse(document.getElementById('itemlist').value);
		if (pointer == "binLocation") {
			$("#binLocation").val("BinLocation - " + qrCodeMessage);
		} else if (pointer == "itemCode") {
			$("#itemCode").val(qrCodeMessage);
		}
	}
	$("#action").change(function (e) {
		e.preventDefault();
		if ($("#action").val() == "move" || $("#action").val() == "inbound") {
			$("#outboundId").hide();
		} else {
			$("#outboundId").show();
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
		$.ajax({
			type: "post",
			url: "/storage/checkItem",
			data: {
				itemCode: $("#itemCode").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				console.log(response)
			}
		});
	});

});