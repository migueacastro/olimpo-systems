<script lang="ts">
    import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
    import { goto } from '$app/navigation';
	import { onlyAdmin, user } from '$lib/stores/auth';
    
    
    export let data: any = {};
    let errors: any = {};
    let cedula: any = '';
	let nombres: any = '';
	let apellidos: any = '';
	let telefono: any = '';
    let email: any = '';
    let password: any = '';
    let confirmPassword: any = '';
    let is_superuser: boolean;
    
    let handleSubmit = () => {
        const endpoint = apiEndpoint + 'tecnicos/' + data.id + '/';
        let formData = new FormData();
        formData.append('nombres', nombres);
        formData.append('apellidos', apellidos);
        formData.append('cedula', cedula);
        formData.append('telefono', telefono);
        formData.append('email', email);
        if (password) {
            formData.append('password', password);
            formData.append('confirmPassword', confirmPassword);
        }
        formData.append('is_superuser', is_superuser.toString());
    
        fetch(endpoint, {
            method: 'PATCH',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                response.json().then(data => errors = data);
            }
        })
        
    };
    
    
    onMount(async () => {
        await onlyAdmin(user);
        let tecnico = await getData(apiEndpoint + 'tecnicos/' + data.id);
        nombres = tecnico?.nombres;
        apellidos = tecnico?.apellidos;
        cedula = tecnico?.cedula;
        telefono = tecnico?.telefono;
        email = tecnico?.email;
        is_superuser = tecnico?.is_superuser;

    
    })
    </script>
    <div class="space-y-10 h-full">
       
        <!-- Header -->
        <div class="mx-5 lg:m-32">
                <header class="flex justify-between items-center">
                    <h1 class="h1 m-5 text-secondary-50 font-bold italic">Editar Técnico</h1>
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
                        class="btn m-4 btn-md variant-filled-primary border border-gray-500"
                        on:click={() => goto('/tecnicos')}
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
        </div>
    </div>