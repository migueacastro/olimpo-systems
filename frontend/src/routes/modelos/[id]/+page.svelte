<script lang="ts">
import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
import { onMount } from 'svelte';
import { getData } from '$lib/components/data';
import { apiEndpoint } from '$lib/endpoint';


export let data: any = {};
let marca: any = '';
let nombre: any = '';

let marcas: any = [];
let errors: any = {};
$: showForm = false;


let handleSubmit = () => {
    const endpoint = apiEndpoint + 'modelos/' + data.id + '/';
    let formData = new FormData();
    formData.append('marca', marca);
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
    let modelo = await getData(apiEndpoint + 'modelos/' + data.id);
    marca = modelo?.marca;
    nombre = modelo?.nombre;
    marcas = await getData(apiEndpoint + 'marcas');

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