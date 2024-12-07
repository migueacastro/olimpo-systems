<script lang="ts">
    import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
    import { goto } from '$app/navigation';
    
    let tipos: any = [];
    
    export let data: any = {};

    let nombre: any = '';
    let errors: any = {};
    $: showForm = false;
    
    
    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'marcas/' + data.id + '/';
        let formData = new FormData();
        formData.append('nombre', nombre);
    
        fetch(endpoint, {
            method: 'PATCH',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                showForm = false;
                window.location.reload();
            } else {
                let data = response.json();
                getModalStore().trigger({
                    type: 'alert',
                    title: 'Error'
                })
            }
        })
        
    };
    
    
    onMount(async () => {
        let tipo = await getData(apiEndpoint + 'marcas/' + data.id);
        nombre = tipo?.nombre;
    
    })
    </script>
    <div class="space-y-10 h-full">
       
        <!-- Header -->
        <div class="mx-5 lg:m-32">
                <header class="flex justify-between items-center">
                    <h1 class="h1 m-5 text-secondary-50 font-bold italic">Editar Marca</h1>
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
                        <a
                            type="button"
                            class="m-4 btn btn-md variant-filled-primary border border-gray-500"
                            href="/marcas"
                        >
                            <span>Volver</span>
                    </a>
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
        </div>
        
    </div>