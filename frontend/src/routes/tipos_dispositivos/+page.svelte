<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
	import { onlyAuthenticated } from '$lib/stores/auth';

    let errors: any = {};
    let nombre: any = '';

    $: showForm = false;

    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'tipos_dispositivos/' ;
        let data = new FormData();
        data.append('nombre', nombre);

        fetch(endpoint, {
            method: 'POST',
            body: data,
        })
        .then(response => {
            if (response.ok) {
                showForm = false;
                window.location.reload();
            } else {
                let data = response.json();
                response.json().then(data => errors = data);
            }
        })
        
    };


    onMount(async () => {
        await onlyAuthenticated();
    })
</script>

<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Tipos Dispositivos</h1>
			<button
				type="button"
				class="btn btn-md variant-filled-primary border border-gray-500"
                on:click={() => showForm = !showForm}
			>
				<span>Agregar</span>
        </button>
            
		</header>
		<!-- Divider -->
		<!-- Component -->
		<Datatable endpoint="tipos_dispositivos" fields={['id', 'nombre']} />
	
        {:else}
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Tipos Dispositivos</h1>
                <button
                    type="button"
                    class="btn btn-md variant-filled-primary border border-gray-500"
                    on:click={() => showForm = !showForm}
                >
                    <span>Volver</span>
                </button>
            </header>
            <!-- Divider -->
            <!-- Component -->
            <form>
                <div class="w-[70%]">
                    
                    <div class="flex flex-row w-full">
                        
                        <div class="mx-4  w-1/3 w-[69.5%]">
                            <label for="nombre" class="text-secondary-100 font-bold">Nombre</label>
                            <input type="text" name="nombre" class="w-full" bind:value={nombre}>
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