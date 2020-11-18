var code, customer, items, itemData = [];
var code = []
var validation = [0, 0, 0]; // [0] outboundid, [1] binlocation, [2] item
// var scanPoint = null;
var pointer, action, itemCode, itemExistm, binlocationExist = null;


function removeItem(a, id) {
	if (confirm('hapus ga ni ?')) {
		$("#" + id).remove()
		code.splice(code.indexOf(a), 1)
		console.log(code)
	}
}

$(document).ready(function () {
	var csrf = $("input[name='csrfmiddlewaretoken']").val();
	var html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
		fps: 10,
		qrbox: 250
	});
	html5QrcodeScanner.render(onScanSuccess);
	$(".overlay").show();
	$(".card-body").hide();


	/*
	============================================================
		fungsi untuk mengambil data yang dibutuhkan scanner
		untuk melakukan verifikasi item yang discan
	============================================================
	*/
	$.ajax({
		type: 'post',
		url: '/storage/getScannerData',
		data: {
			csrfmiddlewaretoken: csrf
		},
		success: function (response) {
			itemData = response
			console.log(itemData)
			$(".overlay").hide();
		},
		fail: function (xhr, textStatus, errorThrown) {
			alert('request failed');
			$(".overlay").hide();
		}
	});

	function onScanSuccess(qrCodeMessage) {
		if (pointer == "binLocation") {
			$("#binLocation").val(qrCodeMessage);
		} else if (pointer == "itemCode") {
			$("#itemCode").val(qrCodeMessage);
		} else if (pointer == "outboundId") {
			$("#outboundId").val(qrCodeMessage);
		}
	}



	/*
	============================================================
		fungsi untuk melakukan testing
	============================================================
	*/
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



	/*
	============================================================
		fungsi saat value berubah pada action selection box
	============================================================
	*/
	$("#action").change(function (e) {
		e.preventDefault();
		$(".card-body").show();
		if ($("#action").val() == "move" || $("#action").val() == "inbound") {
			$("#outboundIdContainer").hide();
			$("#binLocationContainer").show();
			$("#itemCodeContainer").show();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
		} else {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").show();
			$("#itemCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");

		}
	});



	/*
	============================================================
		fungsi untuk mengubah pointer saat melakukan scan 
		qrcode pointer berfungsi agar scanner memasukan data 
		pada element form yang dipilih
	============================================================
	*/
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



	/*
	============================================================
		fungsi untuk memasukan code item hasil scan pada array
		dan membuat element baru, juga mengecek eksistensi item
	============================================================
	*/
	$("#inputItem").click(function (e) {
		e.preventDefault();

		for (i = 0; i < itemData['itembatch'].length; i++) {
			if (itemData['itembatch'][i][1] == $("#itemCode").val()) {
				if (code.includes($("#itemCode").val())) {
					alert("Item telah di scan")
				} else {
					$("#data").append(`<li id="data${i}" onclick="removeItem('${$("#itemCode").val()}','data${i}')">${$("#itemCode").val()}</li>`);
					code.push($("#itemCode").val())
					console.log(code)
				}
				itemExist = 1;
				$("#itemCode").val("");
				break;
			} else {
				itemExist = null
			}
		}
		if (!itemExist) {
			alert("Item tidak tersedia")
			$("#itemCode").val("");
			itemExist = null
		}
	});



	/*
	============================================================
		fungsi untuk mengecek eksistensi binlocation
	============================================================
	*/
	$("#binlocationCheckButton").click(function (e) {
		e.preventDefault();
		for (let i = 0; i < itemData['binlocation'].length; i++) {
			if ($("#binLocation").val() == itemData['binlocation'][i][0]) {
				alert("found")
				binlocationExist = 1
				break;
			} else {
				binlocationExist = null
			}
		}
		if (!binlocationExist) {
			alert("not found")
			$("#binLocation").val("");
			binlocationExist = null
		}
	});



	/*
	============================================================
		fungsi untuk menginput data ke server
	============================================================
	*/
	$("#binLocation").change(function (e) {
		e.preventDefault();
		validation[1] = 0
	});
	$("#outboundId").change(function (e) {
		e.preventDefault();
		validation[0] = 0
	});



	/*
	============================================================
		fungsi untuk mengecek dan mengambil data outbound	
	============================================================
	*/
	$("#outboundCheckButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		$.ajax({
			type: 'post',
			url: '/storage/checkOutbound/',
			data: {
				outboundId: $("#outboundId").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				customer = response['customer']
				items = response['items']
				if (response['customer'] == "" || response['items'] == "") {
					$(".overlay").hide();
				}
				try {
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">customer</td></tr>`);
					$("#outboundData").append(`<tr><td>Nama</td><td id="nama">` + customer[0][0] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[0][1] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[0][2] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[0][3] + `</td></tr>`);
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#outboundData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					for (let i = 0; i < items.length; i++) {
						$("#outboundData").append(`<tr><td>` + items[i][2] + `</td><td>` + items[i][1] + `</td></tr>`);
					}
				} catch (err) {
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">Data tidak ditemukan</td></tr>`);
				}
				$("#itemCodeContainer").show();
				$(".overlay").hide();
			}
		});
	});



	/*
	============================================================
		fungsi untuk mengecek dan mengambil data outbound	
	============================================================
	*/
	$("#confirmButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		if ($("#action").val() == "inbound") {
			$.ajax({
				type: 'post',
				url: '/storage/put/',
				data: {
					binlocation: $("#binLocation").val(),
					itemCode: JSON.stringify(code),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					if (response['binlocation'] == "" || response['itemCode'] == "") {
						$(".overlay").hide();
						alert("error data kosong/tidak ditemukan")
					} else {
						$(".overlay").hide();
						alert("inbound berhasil")
					}
				},
				fail: function (xhr, textStatus, errorThrown) {
					alert('request failed');
					$(".overlay").hide();
				}
			});
			code = [];
			$("#binLocation").val("");

		} else if ($("#action").val() == "move") {
			$.ajax({
				type: 'post',
				url: '/storage/move/',
				data: {
					binlocation: $("#binLocation").val(),
					itemCode: JSON.stringify(code),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					if (response['binlocation'] == "" || response['itemCode'] == "") {
						$(".overlay").hide();
						alert("error data kosong/tidak ditemukan")
					} else {
						$(".overlay").hide();
						alert("move barang berhasil")
					}
				},
				fail: function (xhr, textStatus, errorThrown) {
					alert('request failed');
					$(".overlay").hide();
				}
			});
			code = [];
			$("#binLocation").val("");

		} else if ($("#action").val() == "outbound") {
			$.ajax({
				type: 'post',
				url: '/storage/out/',
				data: {
					outboundId: $("#outboundId").val(),
					itemCode: JSON.stringify(code),
					csrfmiddlewaretoken: csrf
				},
				success: function (response) {
					if (response['outboundId'] == "" || response['itemCode'] == "") {
						$(".overlay").hide();
						alert("error data kosong/tidak ditemukan")
					} else {
						$(".overlay").hide();
						alert("Outbound berhasil")
					}
				},
				fail: function (xhr, textStatus, errorThrown) {
					alert('request failed');
					$(".overlay").hide();
				}
			});
			code = [];
		} else {
			alert("Select option")
		}

	});
	$("#clearButton").click(function (e) {
		e.preventDefault();
		alert("YO WASSSAP")

	});


});