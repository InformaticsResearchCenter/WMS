var customer, itemData = [];
var code = [];
var itemLimit = [];
var items = [];
var validation = {
	"outbound": false,
	"binlocation": false,
	"borrow": false,
	"return": false
};
var pointer, action, itemCode, itemExist, binlocationExist, itemLimitExist, checkLimit, qtyLimit = null;

function removeItem(a, id) {
	if (confirm('remove item ?')) {
		for (let i = 0; i < itemData["item"].length; i++) {
			if (itemData["item"][i]["id"] == a) {
				for (let a = 0; a < itemLimit.length; a++) {
					if (itemLimit[a]["name"] == itemData["item"][i]["name"]) {
						itemLimit[a]["qty"] -= 1;
						break;
					}
				}
				break
			}
		}
		$("#" + id).remove();
		$("#itemData").empty();
		$("#itemData").append(`<tr><td style="font-weight:bold;">Item</td><td style="font-weight:bold;">Qty</td></tr>`);
		for (let i = 0; i < itemLimit.length; i++) {
			if (itemLimit[i]['qty'] > 0) {
				$("#itemData").append(`<tr><td>` + itemLimit[i]['name'] + `</td><td>` + itemLimit[i]['qty'] + `</td></tr>`);
			}
		}

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
	$.ajax({
		type: 'post',
		url: '/app/storage/scanner/getScannerData',
		data: {
			csrfmiddlewaretoken: csrf
		},
		success: function (response) {
			itemData = response
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
			validation["binlocation"] = false;

		} else if (pointer == "itemCode") {
			$("#itemCode").val(qrCodeMessage);
		} else if (pointer == "outboundId") {
			$("#outboundId").val(qrCodeMessage);
			validation["outbound"] = false;
			$("#itemCodeContainer").hide();
			itemLimit = [];
			items = [];
			code = [];
		} else if (pointer == "borrow") {
			$("#borrowCode").val(qrCodeMessage);
			validation["borrow"] = false;
			itemLimit = [];
			items = [];
			code = [];
			$("#itemCodeContainer").hide();
		} else if (pointer == "return") {
			$("#returnCode").val(qrCodeMessage);
			validation["return"] = false;
			itemLimit = [];
			items = [];
			code = [];
			$("#itemCodeContainer").hide();
		}
	}
	$("#binLocation").change(function (e) {
		validation["binlocation"] = false;
		items = [];
		code = [];
		itemLimit = [];
	});
	$("#borrowCode").change(function (e) {
		validation["borrow"] = false;
		$("#itemCodeContainer").hide();
		items = [];
		code = [];
		itemLimit = [];
	});
	$("#outboundId").change(function (e) {
		validation["outbound"] = false;
		$("#itemCodeContainer").hide();
		items = [];
		code = [];
		itemLimit = [];
	});
	$("#returnCode").change(function (e) {
		validation["return"] = false;
		$("#itemCodeContainer").hide();
		items = [];
		code = [];
		itemLimit = [];
	});
	$("#action").change(function (e) {
		e.preventDefault();
		items = [];
		code = [];
		itemLimit = [];
		$("#data").empty();
		$("#itemData").empty();
		$("#itemData").append(`<tr><td>none</td></tr>`);
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
			$("#borrowCode").val("");
			$("#returnCode").val("");
		} else if ($("#action").val() == "outbound") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").show();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
		} else if ($("#action").val() == "borrow") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").show();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
		} else if ($("#action").val() == "return") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").show();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
		} else if ($("#action").val() == "return") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").show();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
		}
	});

	$("#binLocation").click(function (e) {
		e.preventDefault();
		pointer = "binLocation";
	});
	$("#itemCode").click(function (e) {
		e.preventDefault();
		pointer = "itemCode";
	});
	$("#outboundId").click(function (e) {
		e.preventDefault();
		pointer = "outboundId";
	});
	$("#borrowCode").click(function (e) {
		e.preventDefault();
		pointer = "borrow";
	});
	$("#returnCode").click(function (e) {
		e.preventDefault();
		pointer = "return";
	});
	$("#inputItem").click(function (e) {
		e.preventDefault();
		for (i = 0; i < itemData['item'].length; i++) {
			if (itemData['item'][i]['id'] == $("#itemCode").val()) {
				if (code.includes($("#itemCode").val())) {
					alert("Item telah di scan");
				} else {
					if (items != []) {
						for (let a = 0; a < items.length; a++) {
							checkLimit = null;
							if (itemData['item'][i]['itemId'] == items[a]['item']) {
								for (let e = 0; e < itemLimit.length; e++) {
									if (itemLimit[e]['name'] == itemData['item'][i]['name']) {
										if (parseInt(itemLimit[e]['qty']) >= items[a]['quantity']) {
											checkLimit = 1;
											break;
										}
									}
								}
								break;
							}
							checkLimit = 2;
						}
						if (checkLimit == 1) {
							alert("Melebihi kapasitas");
						} else if (checkLimit == 2) {
							alert("Item tidak ada dalam list");
						} else {
							$("#data").append(`<li id="data${i}" onclick="removeItem('${$("#itemCode").val()}','data${i}')">${$("#itemCode").val()} [${itemData['item'][i]['name']}]</li>`);
							code.push($("#itemCode").val());

							if (itemLimit.length == 0) {
								itemLimit.push({
									"name": itemData['item'][i]['name'],
									"id": itemData['item'][i]['itemId'],
									"qty": 1
								});
							} else {
								for (let a = 0; a < itemLimit.length; a++) {
									itemLimitExist = null
									if (itemLimit[a]['name'] == itemData['item'][i]['name']) {
										itemLimit[a]['qty'] += 1;
										itemLimitExist = 1;
										break;
									}
								}
								if (itemLimitExist != 1) {
									itemLimit.push({
										"name": itemData['item'][i]['name'],
										"id": itemData['item'][i]['itemId'],
										"qty": 1
									});
								}
								$("#itemData").empty();
								$("#itemData").append(`<tr><td style="font-weight:bold;">Item</td><td style="font-weight:bold;">Qty</td></tr>`);
								for (let i = 0; i < itemLimit.length; i++) {
									$("#itemData").append(`<tr><td>` + itemLimit[i]['name'] + `</td><td>` + itemLimit[i]['qty'] + `</td></tr>`);
								}
							}
						}
					} else {
						$("#data").append(`<li id="data${i}" onclick="removeItem('${$("#itemCode").val()}','data${i}')">${$("#itemCode").val()} [${itemData['item'][i]['name']}]</li>`);
						code.push($("#itemCode").val());

						if (itemLimit.length == 0) {
							itemLimit.push({
								"name": itemData['item'][i]['name'],
								"id": itemData['item'][i]['itemId'],
								"qty": 1
							});
						} else {
							for (let a = 0; a < itemLimit.length; a++) {
								itemLimitExist = null
								if (itemLimit[a]['name'] == itemData['item'][i]['name']) {
									itemLimit[a]['qty'] += 1;
									itemLimitExist = 1;
									break;
								}
							}
							if (itemLimitExist != 1) {
								itemLimit.push({
									"name": itemData['item'][i]['name'],
									"id": itemData['item'][i]['itemId'],
									"qty": 1
								});
							}
							$("#itemData").empty();
							$("#itemData").append(`<tr><td style="font-weight:bold;">Item</td><td style="font-weight:bold;">Qty</td></tr>`);
							for (let i = 0; i < itemLimit.length; i++) {
								$("#itemData").append(`<tr><td>` + itemLimit[i]['name'] + `</td><td>` + itemLimit[i]['qty'] + `</td></tr>`);
							}
						}
					}
				}
				itemExist = 1;
				$("#itemCode").val("");
				break;
			} else {
				itemExist = null;
			}
		}
		if (!itemExist) {
			alert("Item tidak tersedia")
			$("#itemCode").val("");
			itemExist = null;
		}
	});
	$("#inboundCheckButton").click(function (e) {
		e.preventDefault();
		alert("kakoy")
		$.ajax({
			type: "post",
			url: "/app/storage/scanner/getStockOpname",
			data: {
				inbound: $("#inboundId").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {

			}
		});

	});
	$("#binlocationCheckButton").click(function (e) {
		e.preventDefault();
		validation["binlocation"] = false;
		for (let i = 0; i < itemData['binlocation'].length; i++) {
			if ($("#binLocation").val() == itemData['binlocation'][i]['id']) {
				alert("found");
				binlocationExist = 1;
				validation["binlocation"] = true;
				break;
			} else {
				binlocationExist = null;
			}
		}
		if (!binlocationExist) {
			alert("not found");
			$("#binLocation").val("");
			binlocationExist = null;
		}
	});
	$("#outboundCheckButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		validation["outbound"] = false;
		$.ajax({
			type: 'post',
			url: '/app/storage/scanner/checkOutbound',
			data: {
				outbound: $("#outboundId").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan");
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					$("#outboundData").empty();
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#outboundData").append(`<tr><td>Nama</td><td id="nama">` + customer[0] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[1] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[2] + `</td></tr>`);
					$("#outboundData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[3] + `</td></tr>`);
					$("#outboundData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#outboundData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					items = response['items'];
					for (let index = 0; index < items.length; index++) {
						var itemName;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#outboundData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}
					validation["outbound"] = true;
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
		validation["borrow"] = false;

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
						var itemName;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#borrowData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}
					$("#itemCodeContainer").show();
					validation["borrow"] = true;
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
		validation["return"] = false;
		$.ajax({
			type: 'post',
			url: '/app/storage/scanner/checkReturn',
			data: {
				return: $("#returnCode").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan");
					$("#returnData").empty();
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					customer = Object.values(response['customer'][0]);
					$("#returnData").empty();
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#returnData").append(`<tr><td>Nama</td><td id="nama">` + customer[0] + `</td></tr>`);
					$("#returnData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[1] + `</td></tr>`);
					$("#returnData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[2] + `</td></tr>`);
					$("#returnData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[3] + `</td></tr>`);
					$("#returnData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#returnData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					items = response['items'];
					for (let index = 0; index < items.length; index++) {
						var itemName;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#returnData").append(`<tr><td>` + itemName + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
					}

					$("#itemCodeContainer").show();
					validation["return"] = true;
				}
				$(".overlay").hide();
			},
			fail: function (xhr, textStatus, errorThrown) {
				alert('request failed');
			}
		});
	});
	$("#confirmButton").click(function (e) {
		e.preventDefault();
		if ($("#action").val() == "inbound") {
			if (!validation["binlocation"]) {
				alert("Data Invalid, Binlocation belum di check");
			} else if (code == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
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
						if (response['binlocation'] == "" || response['itemCode'] == "") {
							$(".overlay").hide();
							alert("error data kosong/tidak ditemukan");
						} else {
							$(".overlay").hide();
							alert("inbound berhasil");
						}
					},
					fail: function (xhr, textStatus, errorThrown) {
						alert('request failed');
						$(".overlay").hide();
					}
				});
				code = [];
				$("#binLocation").val("");
			}
		} else if ($("#action").val() == "move") {
			if (!validation["binlocation"]) {
				alert("Data Invalid, Binlocation belum di check");
			} else if (code == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
				$(".overlay").show();
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
							alert("error data kosong/tidak ditemukan");
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
			}

		} else if ($("#action").val() == "outbound") {
			qtyLimit = null
			if (!validation["outbound"]) {
				alert("Data Invalid, Outbound id belum di check");
			} else if (code == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
				if (itemLimit.length == items.length) {
					for (let a = 0; a < items.length; a++) {
						for (let i = 0; i < itemLimit.length; i++) {
							if (itemLimit[i]['id'] == items[a]['item']) {
								if (itemLimit[i]['qty'] != items[a]['quantity']) {
									qtyLimit = 1;
								}
							}
						}
					}
					if (!qtyLimit) {
						$(".overlay").show();
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
									alert("error data kosong/tidak ditemukan");
								} else {
									$(".overlay").hide();
									alert("Outbound berhasil");
								}
							},
							fail: function (xhr, textStatus, errorThrown) {
								alert('request failed');
								$(".overlay").hide();
							}
						});
						code = [];
						itemLimit = [];
						items = [];
					} else {
						alert("jumlah item tidak sesuai");
					}
				} else {
					alert("jumlah item tidak sesuai");
				}
			}

		} else if ($("#action").val() == "return") {
			qtyLimit = null;
			if (!validation["return"]) {
				alert("Data Invalid, return id belum di check");
			} else if (code == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
				if (itemLimit.length == items.length) {
					for (let a = 0; a < items.length; a++) {
						for (let i = 0; i < itemLimit.length; i++) {
							if (itemLimit[i]['id'] == items[a]['item']) {
								if (itemLimit[i]['qty'] != items[a]['quantity']) {
									qtyLimit = 1;
								}
							}
						}
					}
					if (!qtyLimit) {
						$(".overlay").show();
						$.ajax({
							type: 'post',
							url: '/app/storage/scanner/return',
							data: {
								returnId: $("#returnCode").val(),
								itemCode: JSON.stringify(code),
								csrfmiddlewaretoken: csrf
							},
							success: function (response) {
								if (response['returnId'] == "" || response['itemCode'] == "") {
									$(".overlay").hide();
									alert("error data kosong/tidak ditemukan");
								} else {
									$(".overlay").hide();
									alert("return berhasil");
								}
							},
							fail: function (xhr, textStatus, errorThrown) {
								alert('request failed');
								$(".overlay").hide();
							}
						});
						code = [];
						itemLimit = [];
						items = [];
					} else {
						alert("jumlah item tidak sesuai");
					}

				} else {
					alert("jumlah item tidak sesuai");
				}
			}
		} else if ($("#action").val() == "borrow") {
			qtyLimit = null
			if (!validation["borrow"]) {
				alert("Data Invalid, borrow id belum di check");
			} else if (code == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
				if (itemLimit.length == items.length) {
					for (let a = 0; a < items.length; a++) {
						for (let i = 0; i < itemLimit.length; i++) {
							if (itemLimit[i]['id'] == items[a]['item']) {
								if (itemLimit[i]['qty'] != items[a]['quantity']) {
									qtyLimit = 1;
								}
							}
						}
					}
					if (!qtyLimit) {
						$(".overlay").show();
						$.ajax({
							type: 'post',
							url: '/app/storage/scanner/borrow',
							data: {
								borrowId: $("#borrowCode").val(),
								itemCode: JSON.stringify(code),
								csrfmiddlewaretoken: csrf
							},
							success: function (response) {
								if (response['borrowCode'] == "" || response['itemCode'] == "") {
									$(".overlay").hide();
									alert("error data kosong/tidak ditemukan");
								} else {
									$(".overlay").hide();
									alert("borrow berhasil");
								}
							},
							fail: function (xhr, textStatus, errorThrown) {
								alert('request failed');
								$(".overlay").hide();
							}
						});
						code = [];
						itemLimit = [];
						items = [];
					} else {
						alert("jumlah item tidak sesuai");
					}

				} else {
					alert("jumlah item tidak sesuai");
				}
			}
		} else {
			alert("Select option");
		}
	});
	$("#clearButton").click(function (e) {
		e.preventDefault();
		if (confirm("Clear data ?")) {
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
			items = [];
			code = [];
			itemLimit = [];
			$("#itemData").append(`<tr><td>none</td></tr>`);
		}
	});
});