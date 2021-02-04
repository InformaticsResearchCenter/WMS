var customer, itemData = [];
var code = [];
var itemLimit = [];
var items = [];
var brokenItems = [];
var itemStockData = [];
var validation = {
	"outbound": false,
	"binlocation": false,
	"borrow": false,
	"return": false,
	"stockopname": false
};

var pointer, action, itemCode, itemExist, binlocationExist, itemLimitExist, opnameItemExist, checkLimit, qtyLimit = null;

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
		} else if (pointer == "stockOpname") {
			validation["stockopname"] = false;
			$("#rackId").val(qrCodeMessage);

		} else if (pointer == "opname") {
			validation["stockopname"] = false;
			$("#opnameId").val(qrCodeMessage);
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
	$('#rackId').change(function (e) {
		e.preventDefault();
		validation["stockopname"] = false;
		brokenItems = [];
		code = [];
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
			$("#opnameContainer").hide();
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
			$("#opnameContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
			$("#rackId").val("");
			$("#opnameId").val("");
		} else if ($("#action").val() == "borrow") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#opnameContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").show();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
			$("#rackId").val("");
			$("#opnameId").val("");
		} else if ($("#action").val() == "return") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#opnameContainer").hide();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").show();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
			$("#rackId").val("");
			$("#opnameId").val("");
		} else if ($("#action").val() == "opname") {
			$("#binLocationContainer").hide();
			$("#outboundIdContainer").hide();
			$("#opnameContainer").show();
			$("#itemCodeContainer").hide();
			$("#borrowCodeContainer").hide();
			$("#returnCodeContainer").hide();
			$("#binLocation").val("");
			$("#itemCode").val("");
			$("#outboundId").val("");
			$("#borrowCode").val("");
			$("#returnCode").val("");
			$("#rackId").val("");
			$("#opnameId").val("");
		} else {

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
	$("#rackId").click(function (e) {
		e.preventDefault();
		pointer = "stockOpname";

	});
	$("#opnameId").click(function (e) {
		e.preventDefault();
		pointer = "opname"

	});
	$("#inputBrokenButton").click(function (e) {
		e.preventDefault();
		if (itemStockData.length > 0) {
			for (let index = 0; index < itemStockData.length; index++) {
				const e = itemStockData[index];
				if (e.id == $("#opnameId").val()) {
					opnameItemExist = true;
					break;
				}
			}
			if (opnameItemExist == true) {
				if (confirm("Input item to broken list ?")) {
					if (code.includes($("#opnameId").val()) || brokenItems.includes($("#opnameId").val())) {
						alert("item already scanned")
					} else {
						brokenItems.push($("#opnameId").val());
					}
				}
			} else {
				alert('Item listed on this rack');
			}
		} else {
			alert('no item');
		}


	});
	$("#inputNormalButton").click(function (e) {
		e.preventDefault();
		if (itemStockData.length > 0) {
			for (let index = 0; index < itemStockData.length; index++) {
				opnameItemExist = false;
				const e = itemStockData[index];
				if (e.id == $("#opnameId").val()) {
					opnameItemExist = true;
					break;
				}
			}
			if (opnameItemExist == true) {
				if (confirm("Input item to normal list ?")) {
					if (code.includes($("#opnameId").val()) || brokenItems.includes($("#opnameId").val())) {
						alert("item already scanned");
					} else {
						code.push($("#opnameId").val());
					}
				}
			} else {
				alert('Item listed on this rack');
			}
		} else {
			alert('no item');
		}


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
	$("#rackCheckButton").click(function (e) {
		e.preventDefault();
		$(".overlay").show();
		$.ajax({
			type: "post",
			url: "/app/storage/scanner/getStockOpname",
			data: {
				rack: $("#rackId").val(),
				csrfmiddlewaretoken: csrf
			},
			success: function (response) {
				if (typeof response['msg'] != "undefined") {
					alert("Data tidak ditemukan");
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					stockOpname = response
					itemStockData = stockOpname.items
					$("#UniversalData").empty();
					$("#UniversalModalTitle").val("Stock opname");
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#UniversalData").append(`<tr><td>Rack Id</td><td>` + stockOpname.rack[0].id + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Bin total</td><td>` + stockOpname.bin.length + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Item total</td><td>` + stockOpname.itemQuantity + `</td></tr>`);
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#UniversalData").append(`<tr><td>item name</td><td>Qty</td></tr>`);
					for (let index = 0; index < stockOpname.itemdata.length; index++) {
						const element = stockOpname.itemdata[index];

						$("#UniversalData").append(`<tr><td>` + element[0] + `</td><td>` + element[1] + `</td></tr>`);
					}
					$(".overlay").hide();
					validation["stockopname"] = true;
				}
			}
		});
	});

	$("#binlocationCheckButton").click(function (e) {
		e.preventDefault();
		validation["binlocation"] = false;
		for (let i = 0; i < itemData['binlocation'].length; i++) {
			if ($("#binLocation").val() == itemData['binlocation'][i]['binlocation']) {
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
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					console.log(response.customer)
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#UniversalData").append(`<tr><td>Name</td><td id="nama">` + response.customer[0].customer__name + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>province</td><td id="alamat">` + response.customer[0].customer__province + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>city</td><td id="noTelp">` + response.customer[0].customer__city + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>districts</td><td id="tanggal">` + response.customer[0].customer__districts + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>village</td><td id="tanggal">` + response.customer[0].customer__village + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>address</td><td id="tanggal">` + response.customer[0].customer__address + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Postal code</td><td id="tanggal">` + response.customer[0].customer__postalCode + `</td></tr>`);
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#UniversalData").append(`<tr><td>item name</td><td>size</td><td>colour</td><td>qty</td></tr>`);
					items = response['items'];
					for (let index = 0; index < items.length; index++) {
						var itemName;
						var itemSize;
						var itemColour;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								itemSize = itemData['itemlist'][i]['size'];
								itemColour = itemData['itemlist'][i]['colour'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#UniversalData").append(`<tr><td>` + itemName + `</td><td>` + itemSize + `</td><td>` + itemColour + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
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
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					employee = Object.values(response['employee'][0])
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">Employee data</td></tr>`);
					$("#UniversalData").append(`<tr><td>Nama</td><td id="id">` + employee[0] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Alamat</td><td id="nama">` + employee[1] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>no Telp</td><td id="noTelp">` + employee[2] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Tanggal</td><td id="tanggal">` + employee[3] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#UniversalData").append(`<tr><td>item name</td><td>size</td><td>colour</td><td>qty</td></tr>`);
					items = response['items'];
					for (let index = 0; index < items.length; index++) {
						var itemName;
						var itemSize;
						var itemColour;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								itemSize = itemData['itemlist'][i]['size'];
								itemColour = itemData['itemlist'][i]['colour'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#UniversalData").append(`<tr><td>` + itemName + `</td><td>` + itemSize + `</td><td>` + itemColour + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
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
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">` + response['msg'] + `</td></tr>`);
				} else {
					customer = Object.values(response['customer'][0]);
					$("#UniversalData").empty();
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">customer data</td></tr>`);
					$("#UniversalData").append(`<tr><td>Nama</td><td id="nama">` + customer[0] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Alamat</td><td id="alamat">` + customer[1] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>no Telp</td><td id="noTelp">` + customer[2] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td>Tanggal</td><td id="tanggal">` + customer[3] + `</td></tr>`);
					$("#UniversalData").append(`<tr><td colspan="2" style="font-weight:bold;">item list</td></tr>`);
					$("#UniversalData").append(`<tr><td>item name</td><td>size</td><td>colour</td><td>qty</td></tr>`);
					items = response['items'];
					for (let index = 0; index < items.length; index++) {
						var itemName;
						var itemSize;
						var itemColour;
						for (let i = 0; i < itemData['itemlist'].length; i++) {
							if (itemData['itemlist'][i]['id'] == items[index]['item']) {
								itemName = itemData['itemlist'][i]['name'];
								itemSize = itemData['itemlist'][i]['size'];
								itemColour = itemData['itemlist'][i]['colour'];
								break;
							} else {
								itemName = "undefined";
							}
						}
						$("#UniversalData").append(`<tr><td>` + itemName + `</td><td>` + itemSize + `</td><td>` + itemColour + `</td><td>` + items[index]['quantity'] + `</td></tr>`);
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
		} else if ($("#action").val() == "opname") {
			if (!validation["stockopname"]) {
				alert("Data Invalid, rack id belum di check");
			} else if (code == "" && brokenItems == "") {
				alert("Data Invalid, belum ada item yang di scan");
			} else {
				$(".overlay").show();

				$.ajax({
					type: 'post',
					url: '/app/storage/scanner/stockOpname',
					data: {
						rackid: stockOpname.rack[0].id,
						item: JSON.stringify(stockOpname.items),
						normal: JSON.stringify(code),
						broken: JSON.stringify(brokenItems),
						csrfmiddlewaretoken: csrf
					},
					success: function (response) {

						$(".overlay").hide();
						alert("stock opname " + stockOpname.rack[0].id + " berhasil");

					},
					fail: function (xhr, textStatus, errorThrown) {
						alert('request failed');
						$(".overlay").hide();
					}
				});
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