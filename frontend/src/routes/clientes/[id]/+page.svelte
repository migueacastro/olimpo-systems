<script lang="ts">
    import { getModalStore, initializeStores } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
    import { goto } from '$app/navigation';
    
    
    export let data: any = {};
    let nombres: any = '';
    let apellidos: any = '';
    let cedula: any = '';
    let telefono: any = '';
    let servicios: any = [];
    let errors: any = {};
    let tecnicos: any = [];

    async function findTecnicoById(id: any) {
        let tecnicos = await getData(apiEndpoint + 'tecnicos');
;
        let tecnico = await tecnicos.find((tecnico: any) => tecnico.id == id);
        return tecnico.nombres + " " + tecnico.apellidos;
    }


    
    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'clientes/' + data.id + '/';
        let formData = new FormData();
        formData.append('nombres', nombres);
        formData.append('apellidos', apellidos);
        formData.append('cedula', cedula);
        formData.append('telefono', telefono);
    
        fetch(endpoint, {
            method: 'PATCH',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
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
        let cliente = await getData(apiEndpoint + 'clientes/' + data.id);
        nombres = cliente?.nombres;
        apellidos = cliente?.apellidos;
        cedula = cliente?.cedula;
        telefono = cliente?.telefono;
        servicios = cliente?.servicios;
    
    })
    </script>
    <div class="space-y-10 h-full">
        
        <!-- Header -->
        <div class="mx-5 lg:m-32">
                <header class="flex justify-between items-center">
                    <h1 class="h1 m-5 text-secondary-50 font-bold italic">Editar Cliente</h1>

                </header>
                <!-- Divider -->
                <!-- Component -->
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
                            href="/clientes"
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
                <!--
                {#if servicios.length > 0}
                <table class="table table-hover table-compact table-auto overflow-x-scroll">
                    <thead>
                        <tr>
                            <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Fecha</th>
                            <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Tecnico</th>
                            <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Dispositivos</th>

                        </tr>
                    </thead>
                    <tbody class="variant-filled-secondary">
                       
                        {#each servicios as servicio}
                           
                            <tr >
                                 
                                <td class="border-gray-100 font-bold text-center">
                                    {servicio?.fecha_entrega}
                                </td>             
                                <td class="border-gray-100 font-bold text-center">
                                    {findTecnicoById(servicio?.tecnico_id)}
                                </td>
                                <td> <a href="/servicios/{servicio.id}">Dispositivos</a></td>
                            
                            </tr>
                        {/each}
                        
                    </tbody>  
                </table>
            {/if}
            -->
        </div>
    </div>