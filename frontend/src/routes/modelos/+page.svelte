<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
	import { onlyAuthenticated } from '$lib/stores/auth';
    initializeStores();
	let tipos: any = [];

    let errors: any = {};
    let nombre: any = '';
    let marca: any = '';
    let marcas: any = [];

    let modelos: any = [];
    $: showForm = false;

    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'modelos/' ;
        let data = new FormData();
        data.append('marca', marca);
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
        marcas = await getData(apiEndpoint + 'marcas');
        marca = marcas[0]?.id;
        modelos = await getData(apiEndpoint + 'modelos');
    })
</script>

<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Modelos: {modelos?.length}</h1>
            <div class="flex flex-row">
                <button
				type="button"
				class="btn btn-md variant-filled-primary border border-gray-500"
				on:click={() => showForm = !showForm}
			>
				<span>Agregar Modelos</span>
            </button>
            <a
                    class="mx-4 btn btn-md variant-filled-primary border border-gray-500"
                    type="button"
                    href="/marcas"
                >
                    <span>Marcas</span>
                </a>
            
            </div>
			
		</header>
		<!-- Divider -->
		<!-- Component -->
		<Datatable endpoint="modelos" fields={['id', 'nombre','nombre_marca']} />
	
        {:else}
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Modelos</h1>
            </header>
            <!-- Divider -->
            <!-- Component -->
            <form>
                <div class="w-[70%]">
                    
                    <div class="flex flex-row w-full">
                        
                        <div class="mx-4  w-1/3">
                            <label for="nombre" class="text-secondary-100 font-bold">Nombre</label>
                            <input type="text" name="nombre" class="w-full" bind:value={nombre}>
                        </div>
                        <div class="mx-4 w-1/3">
                            <label for="marca" class="text-secondary-100 font-bold" >Marca</label>
                            <select name="marca" id="marca" bind:value={marca} class="w-full">
                                {#each marcas as marca}
                                    <option value={marca.id}>{marca.nombre}</option>
                                {/each}
                            </select>                       
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