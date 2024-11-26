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
    
    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'tecnicos/' + data.id + '/';
        let formData = new FormData();
        formData.append('nombres', nombres);
        formData.append('apellidos', apellidos);
        formData.append('cedula', cedula);
        formData.append('telefono', telefono);
    
        fetch(endpoint, {
            method: 'PUT',
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
        let tecnico = await getData(apiEndpoint + 'tecnicos/' + data.id);
        nombres = tecnico?.nombres;
        apellidos = tecnico?.apellidos;
        cedula = tecnico?.cedula;
        telefono = tecnico?.telefono;
    
    })
    </script>
    <div class="space-y-10 h-full">
       
        <!-- Header -->
        <div class="mx-5 lg:m-32">
                <header class="flex justify-between items-center">
                    <h1 class="h1 m-5 text-secondary-50 font-bold italic">Editar Técnico</h1>
                    <button
                        type="button"
                        class="btn btn-md variant-filled-primary border border-gray-500"
                        on:click={() => goto('/tecnicos')}
                    >
                        <span>Volver</span>
                    </button>
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
                    <button
                    type="button"
                    class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                    on:click={handleSubmit}
                    >Guardar</button>       
                </form>
        </div>
    </div>