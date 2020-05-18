class Loader {

	constructor(server_uri) {

		this.server_uri = server_uri;

	}

	call(method, url, query_params, form=null) {

		return new Promise((resolve, reject) => {

			let request = new XMLHttpRequest();

			request.open(
				method.toUpperCase(),
				this.server_uri + url + (query_params ? '?' : '') +
				Object.keys(query_params).map(
					key => `${key}=${query_params[key]}`).join('&'),
				true);

			request.onreadystatechange = event => {
				if (request.readyState == 4) {
					try{
						let result = JSON.parse(request.response);
					// some error while JSON parsing occured
					} catch(e) { reject(result.response); };
					// otherwise just return result
					resolve(result.response);
				}
			}

			// you may also pass FormData class which will be sent to server.
			// use for file uploading.
			if (form) request.send(form);
			else request.send();

		});

	}

}

const loader = new Loader('http://localhost:8080/api/v1/');
