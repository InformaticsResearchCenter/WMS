var code, customer, items, itemData = [];
var code = []
var itemLimit = []
var validation = [0, 0, 0]; // [0] outboundid, [1] binlocation, [2] item
// var scanPoint = null;
var pointer, action, itemCode, itemExist, binlocationExist, itemLimitExist = null;


function removeItem(a, id) {
	if (confirm('remove item ?')) {
		for (let i = 0; i < itemData["item"].length; i++) {
			if (itemData["item"][i]["id"] == a) {
				for (let a = 0; a < itemLimit.length; a++) {
					console.log(itemLimit[a]["name"])
					console.log(itemData["item"][i]["name"])
					if (itemLimit[a]["name"] == itemData["item"][i]["name"]) {
						itemLimit[a]["qty"] -= 1
						break
					}
				}
				break
			}
		}
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
		url: '/app/storage/scanner/getScannerData',
		data: {
			csrfmiddlewaretoken: csrf
		},
		success: function (response) {
			itemData = response
			console.log(itemData['itemlist'])
			console.log(itemData['item'])
			console.log(itemData['binlocation'])
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
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrow").val("");
			$("#return").val("");
		} else if ($("#action").val() == "outbound") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").show();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrow").val("");
			$("#return").val("");
		} else if ($("#action").val() == "borrow") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").show();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrow").val("");
			$("#return").val("");
		} else if ($("#action").val() == "return") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").show();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrow").val("");
			$("#return").val("");
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
	$("#borrowCode").click(function (e) {
		e.preventDefault();
		pointer = "borrow"
	});
	$("#returnCode").click(function (e) {
		e.preventDefault();
		pointer = "return"
	});



	/*
	============================================================
		fungsi untuk memasukan code item hasil scan pada array
		dan membuat element baru, juga mengecek eksistensi item
	============================================================
	*/
	$("#inputItem").click(function (e) {
		e.preventDefault();
		console.log(itemData['item'])
		console.log(code)
		for (i = 0; i < itemData['item'].length; i++) {
			if (itemData['item'][i]['id'] == $("#itemCode").val()) {
				console.log(`DATA : ` + itemData['item'][i]['name'])
				if (code.includes($("#itemCode").val())) {
					alert("Item telah di scan")
				} else {
					$("#data").append(`<li id="data${i}" onclick="removeItem('${$("#itemCode").val()}','data${i}')">${$("#itemCode").val()} [${itemData['item'][i]['name']}]</li>`);
					code.push($("#itemCode").val())
					if (itemLimit.length == 0) {
						itemLimit.push({
							"name": itemData['item'][i]['name'],
							"qty": 1
						})
					} else {
						for (let a = 0; a < itemLimit.length; a++) {
							itemLimitExist = null
							console.log(`DATA LOOP : ` + itemLimit[a]['name'], itemLimit[a]['name'] == itemData['item'][i]['name'])
							if (itemLimit[a]['name'] == itemData['item'][i]['name']) {
								itemLimit[a]['qty'] += 1
								itemLimitExist = 1
								break
							}
						}
						console.log(itemLimitExist)
						if (itemLimitExist != 1) {
							itemLimit.push({
								"name": itemData['item'][i]['name'],
								"qty": 1
							})
						}
						$("#itemData").empty();
						$("#itemData").append(`<tr><td style="font-weight:bold;">Item</td><td style="font-weight:bold;">Qty</td></tr>`);
						for (let i = 0; i < itemLimit.length; i++) {
							$("#itemData").append(`<tr><td>` + itemLimit[i]['name'] + `</td><td>` + itemLimit[i]['qty'] + `</td></tr>`);
						}

					}
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
		console.log(itemData['binlocation'][1]['id'])
		for (let i = 0; i < itemData['binlocation'].length; i++) {
			console.log(itemData['binlocation'][i]['id'])
			if ($("#binLocation").val() == itemData['binlocation'][i]['id']) {
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
			url: '/app/storage/scanner/checkOutbound',
			data: {
				outbound: $("#outboundId").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan")
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					console.log(response)
					customer = Object.values(response['customer'][0])
					console.log(customer)
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#outboundData").append(`<tr><td>Nama</td><td id="nama">` + customer[0] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[1] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[2] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[3] + `</td></tr>`);
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#outboundData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					items = response['items']
					for (let index = 0; index < items.length; index++) {
						var itemName
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name']
								break
							} else {
								console.log(itemData['itemlist'][i]['id'], items[index]['item'])
								itemName = "undefined"
							}
						}
						$("#outboundData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}

					$("#itemCodeContainer").show();
				}
				$(".overlay").hide();
			},
			fail: function (xhr, textStatus, errorThrown) {
				alert('request failed');
			}


		});
	});
	$("#borrowCheckButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		$.ajax({
			type: 'post',
			url: '/app/storage/scanner/checkBorrow',
			data: {
				borrow: $("#borrowCode").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan")
					$("#borrowData").empty();
					$("#borrowData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					employee = Object.values(response['employee'][0])
					console.log(employee)
					$("#borrowData").empty();
					$("#borrowData").append(`<tr><td colspan="2" style="font-weight:bold;">Employee data</td></tr>`);
					$("#borrowData").append(`<tr><td>Nama</td><td id="nama">` + employee[0] + `</td></tr>`);
					$("#borrowData").append(`<tr><td>Alamat</td><td id="alamat">` + employee[1] + `</td></tr>`);
					$("#borrowData").append(`<tr><td>no Telp</td><td id="noTelp">` + employee[2] + `</td></tr>`);
					$("#borrowData").append(`<tr><td>Tanggal</td><td id="tanggal">` + employee[3] + `</td></tr>`);
					$("#borrowData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#borrowData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					items = response['items']
					for (let index = 0; index < items.length; index++) {
						var itemName
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name']
								break
							} else {
								console.log(itemData['itemlist'][i]['id'], items[index]['item'])
								itemName = "undefined"
							}
						}
						$("#borrowData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}
					$("#itemCodeContainer").show();
				}
				$(".overlay").hide();
			},
			fail: function (xhr, textStatus, errorThrown) {
				alert('request failed');
			}


		});
	});
	$("#returnCheckButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		$.ajax({
			type: 'post',
			url: '/app/storage/scanner/checkReturn',
			data: {
				return: $("#returnCode").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan")
					$("#returnData").empty();
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					console.log(response)
					customer = Object.values(response['customer'][0])
					console.log(customer)
					$("#returnData").empty();
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#returnData").append(`<tr><td>Nama</td><td id="nama">` + customer[0] + `</td></tr>`);
					$("#returnData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[1] + `</td></tr>`);
					$("#returnData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[2] + `</td></tr>`);
					$("#returnData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[3] + `</td></tr>`);
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#returnData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					items = response['items']
					for (let index = 0; index < items.length; index++) {
						var itemName
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name']
								break
							} else {
								console.log(itemData['itemlist'][i]['id'], items[index]['item'])
								itemName = "undefined"
							}
						}
						$("#returnData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}

					$("#itemCodeContainer").show();
				}
				$(".overlay").hide();
			},
			fail: function (xhr, textStatus, errorThrown) {
				alert('request failed');
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
				url: '/app/storage/scanner/put',
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
				url: '/app/storage/scanner/move',
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
				url: '/app/storage/scanner/out',
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
		} else if ($("#action").val() == "return") {
			$.ajax({
				type: 'post',
				url: '/app/storage/scanner/return',
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
		} else if ($("#action").val() == "borrow") {
			$.ajax({
				type: 'post',
				url: '/app/storage/scanner/borrow',
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
		$(".overlay").show();

		$.ajax({
			type: 'post',
			url: '/app/storage/scanner/put',
			data: {
				binlocation: $("#binLocation").val(),
				itemCode: JSON.stringify(code),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				alert("Cooo")
				$(".overlay").hide();
			},
			fail: function (xhr, textStatus, errorThrown) {
				alert('request failed');
				$(".overlay").hide();
			}
		});

	});


});