<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { apiEndpoint } from '$lib/endpoint';
    initializeStores();
    import { getModalStore } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { onlyAuthenticated } from '$lib/stores/auth';
	
	let id: any = '';
	let cedula: any = '';
	let nombres: any = '';
	let apellidos: any = '';
	let telefono: any = '';

	$: showForm = false;
    let errors: any = {};

	function handleSubmit() {
        const endpoint = apiEndpoint + 'clientes' + '/';
        let data = new FormData();
        data.append('cedula', cedula);
        data.append('nombres', nombres);
        data.append('apellidos', apellidos);
        data.append('telefono', telefono);

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
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Clientes</h1>
			<button
                    on:click={() => showForm = !showForm}
					type="button"
					class="btn btn-md variant-filled-primary border border-gray-500"
				>
				
                <span>Agregar Cliente</span>
				</button>

		</header>
		<!-- Component -->
		<Datatable endpoint="clientes" fields={['id', 'cedula', 'nombres', 'apellidos', 'telefono']} />
        {:else}
        <form>
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Clientes</h1>

            </header>
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
            </div>
            <div class="flex flex-row">
                <button
                type="button"
                class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                on:click={handleSubmit}
                >Guardar</button>
                <button
                            class="m-4 btn btn-md variant-filled-primary border border-gray-500"
                            on:click={() => showForm = !showForm}
                        >
                            <span>Volver</span>
            </button>
            </div>
        </form>
        <div class="mx-4 flex flex-col w-[48.5%] bg-error-50">
            {#if Object.keys(errors).length > 0} 
                <ul class="w-full p-4">
                    {#each Object.entries(errors) as error}
                    <li class="text-error-500 capitalize">{error[0]}: {error[1]}</li>
                    {/each}
                </ul> 
            {/if}
        </div>
        {/if}
	</div>
	
</div>