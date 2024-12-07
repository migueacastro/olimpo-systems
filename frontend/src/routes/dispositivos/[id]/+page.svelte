<script lang="ts">
    import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
    import { goto } from '$app/navigation';

    let tipos: any = [];

    export let data: any = {};
    let selectedTipo = '';
    let marca: any = '';
    let modelo: any = '';

    let serial: any = '';
    let imeis: any = {};
    let status: any = '';
    let tipo: any = '';

    let imei1: any = '';
    let imei2: any = '';
    let errors: any = {};
    $: showForm = false;
    let marcas: any = [];
    let modelos: any = [];
    function filterModelos(marca: any) {
        return marcas.find((m: any) => m.id === marca)?.modelos || [];
    }
    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'dispositivos/' + data.id + '/';
        let formData = new FormData();
        formData.append('marca', marca);
        formData.append('modelo', modelo);
        formData.append('serial', serial);
        formData.append('tipo', tipos.find((t: any) => t.id === tipo).id);
        formData.append('imeis', JSON.stringify({data: [imei1, imei2]}));

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
        let dispositivo = await getData(apiEndpoint + 'dispositivos/' + data.id);
        marcas = await getData(apiEndpoint + 'marcas');
        modelos = await getData(apiEndpoint + 'modelos');
        marca = dispositivo?.marca;
        modelo = dispositivo?.modelo;
        serial = dispositivo?.serial;
        imei1 = dispositivo?.imeis?.data[0];
        imei2 = dispositivo?.imeis?.data[1];

        tipos = await getData(apiEndpoint + 'tipos_dispositivos');
        tipo = dispositivo?.tipo;

    })
</script>
<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Editar Dispositivo</h1>
            </header>
            <!-- Divider -->
            <!-- Component -->
            <form>
                <div class="w-[70%]">
                    
                    <div class="flex flex-row w-full">
                        
                        <div class="mx-4  w-1/3">
                            <label for="marca" class="text-secondary-100 font-bold">Marca</label>
                            <select name="marca" id="marca" bind:value={marca} class="w-full">
                                {#each marcas as marca}
                                    <option value={marca.id}>{marca.nombre}</option>
                                {/each}
                            </select>
                        </div>
                        <div class="mx-4  w-1/3">
                            <label for="modelo" class="text-secondary-100 font-bold">Modelo</label>
                            <select name="modelo" id="modelo" bind:value={modelo} class="w-full">
                                {#each filterModelos(marca) as modelo}
                                    <option value={modelo.id}>{modelo.nombre}</option>
                                {/each}
                            </select>
                        </div>
                    </div>
                    <div class="flex flex-row w-full">
                        <div class="mx-4 w-1/3">
                            <label for="tipo" class="text-secondary-100 font-bold" >Tipo de Dispositivo</label>
                            <select name="tecnico" id="tecnico" bind:value={tipo} class="w-full">
                                {#each tipos as tipo}
                                    <option value={tipo.id}>{tipo.nombre}</option>
                                {/each}
                            </select>
                             
                        </div>
                        <div class="mx-4 w-1/3">
                            <label for="serial" class="text-secondary-100 font-bold">Serial</label>
                            <input type="text" name="serial" class="w-full" bind:value={serial}>
                        </div>
                    </div>
                    
                    
                    <div class="flex flex-row ">
                        
                        {#if tipo === 1}

                            <div class="mx-4 w-1/3">
                                <label for="imei-1" class="text-secondary-100 font-bold">IMEI 1</label>
                                <input type="text" name="imei-1" class="w-full" bind:value={imei1}>
                            </div>
                            <div class="mx-4 w-1/3">
                                <label for="imei-2" class="text-secondary-100 font-bold">IMEI 2</label>
                                <input type="text" name="imei-2" class="w-full" bind:value={imei2}>
                            </div>

                        {/if}
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
                            href="/dispositivos"
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