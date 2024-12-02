<script lang="ts">
    import { goto } from '$app/navigation';
    import { authenticateUser } from '$lib/stores/auth';
    import { apiEndpoint } from '$lib/endpoint';
    let email = '';
    let password = '';
    let errors: any = {};
    const handleSubmit = async () => {
        let endpoint = `${apiEndpoint}login/`;
        
        await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                
                
            },
            body: JSON.stringify({
                'email': email,
                'password': password
            }),
            credentials: 'include',
        })
        .then(response => response.json()
        .then(data => ({status: response.status, body: data})))
        .then(data => {
            if (data.status === 200) {
                // I added this line so that the navbar updates instantly, otherwise it would take a refresh to update it
                goto('/');
                authenticateUser();
            } else {
                errors = data.body;
                console.log(data);
            }
        })
    };
</script>
<header class="text-center py-4 text-white mt-[5rem]">
	<div class="text-center mb-2 text-3xl font-bold">Iniciar Sesión</div>
</header>
<div class="w-1/2 mx-auto p-6 space-y-6 text-left">
	<form class="space-y-4"  on:submit|preventDefault={handleSubmit}>
		<label class="label text-secondary-100 font-bold">
			<span>Email</span>
			<input type="email" placeholder="" class="input text-black" bind:value={email}/>
		</label>
		<label class="label text-secondary-100 font-bold">
			<span>Contraseña</span>
			<input type="password" placeholder="" class="input text-black" bind:value={password}/>
		</label>
		<button class="btn variant-filled-primary w-full">Iniciar Sesión</button>
	</form>
</div>