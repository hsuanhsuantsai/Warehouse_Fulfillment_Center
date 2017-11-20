class Warehouse {
	constructor(API) {
		this.api = API;
	}
	// get warehouse inventory status
	items(callback, sku) {
		if (sku != '')
			sku = sku + '/'
		const url = 'https://stack-warehouse.herokuapp.com/' + this.api + '/inventory/' + sku;
		fetch(url).then(this.parseResponse).then(this.storeItems).then(callback);
	}

	parseResponse(response) { 
		return response.json(); 
	}

	storeItems(data) {
		let res = []
		const keyArray = Object.keys(data)
		if (keyArray.length > 0) {
			keyArray.forEach( key => {
				const obj = data[key]
				res.push(obj)
			})
		}
		return res;
	}
}

