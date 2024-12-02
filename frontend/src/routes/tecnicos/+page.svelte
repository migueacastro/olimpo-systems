<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { apiEndpoint } from '$lib/endpoint';
    initializeStores();
	import { onMount } from 'svelte';
	import { onlyAuthenticated } from '$lib/stores/auth';
	import { user } from '$lib/stores/auth';
	let id: any = '';
	let cedula: any = '';
	let nombres: any = '';
	let apellidos: any = '';
	let telefono: any = '';
    let email: any = '';
    let password: any = '';
    let confirmPassword: any = '';
    let is_superuser: boolean;

	$: showForm = false;
    let errors: any = {};

	function handleSubmit() {
        const endpoint = apiEndpoint + 'tecnicos' + '/';
        let data = new FormData();
        data.append('cedula', cedula);
        data.append('nombres', nombres);
        data.append('apellidos', apellidos);
        data.append('telefono', telefono);
        data.append('email', email);
        data.append('password', password);
        data.append('confirmPassword', confirmPassword);
        data.append('is_superuser', 'true');
        fetch(endpoint, {
            method: 'POST',
            body: data,
        })
        .then(response => {
            if (response.ok) {
                showForm = false;
                window.location.reload();
            } else {
                response.json().then(data => errors = data);
            }
        })
    }
    onMount(async () => {
        await onlyAuthenticated();
    })
</script>

<div class="space-y-10">
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Técnicos</h1>
            {#if $user.is_superuser}
			<button
                    on:click={() => showForm = !showForm}
					type="button"
					class="btn btn-md variant-filled-primary border border-gray-500"
				>
				
                <span>Agregar</span>
				</button>
            {/if}
		</header>
		<!-- Component -->
		<Datatable endpoint="tecnicos" fields={['id', 'cedula', 'email', 'nombres', 'apellidos', 'telefono']} />
        {:else}
        <header class="flex justify-between items-center">
            <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Técnicos</h1>
            
        </header>
        <form>
            <div class="w-[70%]">
                
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4  w-1/3">
                        <label for="nombres" class="text-secondary-100 font-bold">Nombres</label>
                        <input type="text" name="nombres" class="w-full" bind:value={nombres}>
                    </div>
                    <div class="mx-4  w-1/3">
                        <label for="apellidos" class="text-secondary-100 font-bold">Apellidos</label>
                        <input type="text" name="apellidos" class="w-full" bind:value={apellidos}>
                    </div>
                </div>
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4  w-1/3">
                        <label for="cedula" class="text-secondary-100 font-bold">Cedula</label>
                        <input type="text" name="cedula" class="w-full" bind:value={cedula}>
                    </div>
                    <div class="mx-4  w-1/3">
                        <label for="telefono" class="text-secondary-100 font-bold">Teléfono</label>
                        <input type="text" name="telefono" class="w-full" bind:value={telefono}>
                    </div>
                </div>
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4 w-[69.5%]">
                        <label for="email" class="text-secondary-100 font-bold">Email</label>
                        <input type="text" name="email" class="w-full" bind:value={email}>
                    </div>
                </div>
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4  w-1/3">
                        <label for="password" class="text-secondary-100 font-bold">Confirmar Contraseña</label>
                        <input type="password" name="password" class="w-full" bind:value={password}>
                    </div>
                    <div class="mx-4  w-1/3">
                        <label for="confirm-password" class="text-secondary-100 font-bold">Contraseña</label>
                        <input type="password" name="confirm-password" class="w-full" bind:value={confirmPassword}>
                    </div>
                </div>
                <div class="ml-[1rem] mt-2">
                    <input type="checkbox" id="is_superuser" name="is_superuser" class="mr-2" bind:checked={is_superuser}>¿Es administrador?
                </div>
                
            </div>
            <div class="flex flex-row">
                <button
                type="button"
                class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                on:click={handleSubmit}
                >Guardar</button>
                <button
                    type="button"
                    class="m-4 btn btn-md variant-filled-primary border border-gray-500"
                    on:click={() => showForm = !showForm}
                >
                    <span>Volver</span>
                </button>
            </div>
            <div class="mx-4 flex flex-col w-[48.5%] bg-error-50">
                {#if Object.keys(errors).length > 0} 
                    <ul class="w-full p-4">
                        {#each Object.entries(errors) as error}
                        <li class="text-error-500 capitalize">{error[0]}: {error[1]}</li>
                        {/each}
                    </ul> 
                {/if}
            </div>

        </form>
        {/if}
	</div>
	
</div>