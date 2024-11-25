<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
    initializeStores();
	let tecnicos: any = [];
    let clientes: any = [];
    let tiposDispositivos: any = [];


    let selectedTecnico = '';
    let nombres: any = '';
    let apellidos: any = '';
    let cedula: any = '';
    let telefono: any = '';

    let cliente: any = '';
    let tecnico: any = ''; 
    let tipo: any = '1';

    function findClientByCedula(cedula: any) {
        if (!cedula) return;
        for (let client of clientes) {
            if (client.cedula === cedula) {
                nombres = client.nombres;
                apellidos = client.apellidos;
                telefono = client.telefono;
                return;
            }
        }
    }
    $: showForm = false;
    onMount(async () => {
        tecnicos = await getData(apiEndpoint + 'tecnicos');
        clientes = await getData(apiEndpoint + 'clientes');
        tiposDispositivos = await getData(apiEndpoint + 'tipos_dispositivos');
        tipo = tiposDispositivos[0]?.id;
        tecnico = tecnicos[0]?.id;
    })
</script>

<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Servicios</h1>
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
		<Datatable endpoint="servicios" fields={['id', 'fecha_salida','fecha_entrada', 'cliente', 'tecnico','falla_reportada', 'reparacion_efectuada', 'dispositivos', 'observaciones']} />
	
        {:else}
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Servicios</h1>
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
                    <div class="flex flex-row">
                        <div class="mx-4 w-[50%]">
                            <label for="nombres" class="text-secondary-100 font-bold">Nombres</label>
                            <input type="text" name="nombres" class="w-full">
                        </div>
                        <div class="mx-4  w-[50%]">
                            <label for="apellidos" class="text-secondary-100 font-bold">Apellidos</label>
                            <input type="text" name="apellidos" class="w-full">
                        </div>
                    </div>
                    
                    <div class="flex flex-row w-full">
                        <div class="mx-4 w-1/3">
                            <label for="cedula" class="text-secondary-100 font-bold">Cedula</label>
                            <input type="text" name="cedula" class="w-full">
                        </div>
                        <div class="mx-4 w-1/3" >
                            <label for="telefono" class="text-secondary-100 font-bold">Nro. Teléfono</label>
                            <input type="text" name="telefono" class="w-full">
                        </div>
                        <div class="mx-4 w-1/3">
                            <label for="tecnico" class="text-secondary-100 font-bold" >Tecnico</label>
                            <select name="tecnico" id="tecnico" bind:value={tecnico} class="w-full">
                                {#each tecnicos as tecnico }
                                    <option value={tecnico.id}>{tecnico.nombres} {tecnico.apellidos}</option>
                                {/each}
                            </select>
                        </div>
                        
                    </div>
                    
                    <div class="flex flex-row w-full">
                        <div class="mx-4 w-1/3">
                            <label for="tipo" class="text-secondary-100 font-bold" >Tipo de Dispositivo</label>
                            <select name="tecnico" id="tecnico" bind:value={tipo} class="w-full">
                                {#each tiposDispositivos as tipo}
                                    <option value={tipo.id}>{tipo.nombre}</option>
                                {/each}
                            </select>
                        </div>
                        <div class="mx-4  w-1/3">
                            <label for="marca" class="text-secondary-100 font-bold">Marca</label>
                            <input type="text" name="marca" class="w-full">
                        </div>
                        <div class="mx-4  w-1/3">
                            <label for="modelo" class="text-secondary-100 font-bold">Modelo</label>
                            <input type="text" name="modelo" class="w-full">
                        </div>
                    </div>
                    <div class="flex flex-row ">
                        <div class="mx-4 w-1/3">
                            <label for="serial" class="text-secondary-100 font-bold">Serial</label>
                            <input type="text" name="serial" class="w-full">
                        </div>
                        {#if tipo === 1}

                            <div class="mx-4 w-1/3">
                                <label for="imei-1" class="text-secondary-100 font-bold">IMEI 1</label>
                                <input type="text" name="imei-1" class="w-full">
                            </div>
                            <div class="mx-4 w-1/3">
                                <label for="imei-2" class="text-secondary-100 font-bold">IMEI 2</label>
                                <input type="text" name="imei-2" class="w-full">
                            </div>

                        {/if}
                    </div>
                    <div class="flex flex-row w-full">
                        <div class="mx-4 w-1/2">
                            <label for="falla_reportada" class="text-secondary-100 font-bold">Falla Reportada</label>
                            <textarea name="falla_reportada" id="falla_reportada" class="w-full"></textarea>
                        </div>
                        <div class="mx-4 w-1/2">
                            <label for="reparacion_efectuada" class="text-secondary-100 font-bold">Reparación Efectuada</label>
                            <textarea name="reparacion_efectuada" id="reparacion_efectuada" class="w-full"></textarea>
                        </div>
                    </div>
                </div>
                <button
                type="button"
                class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                on:click={() => showForm = !showForm}
                >Guardar</button>
                

                
            </form>

        {/if}
    </div>
	
</div>