export async function getData(endpoint: string) {
    const response = await fetch(endpoint, {
		method: 'GET',
		headers: {
			"ngrok-skip-browser-warning": "69420"
		}
	});

    const data = await response.json();
    return data;
}