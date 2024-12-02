<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
    import { getData } from '$lib/components/data';
    import { apiEndpoint } from '$lib/endpoint';
	import { onlyAuthenticated } from '$lib/stores/auth';
    initializeStores();
	let tecnicos: any = [];
    let clientes: any = [];
    let tiposDispositivos: any = [];
    export let data: any = [];

    interface Dispositivo {
        marca: string | null;
		modelo: string | null;
		serial: string | null;
		imeis: any;
		tipo: string | null;
    }
    interface DispositivoServicio {
		dispositivo: any;
        reparaciones: any;
        costo: number | null;
        status: string | null;
	}
	let dispositivos: Array<DispositivoServicio> = [{dispositivo: {marca: '', modelo: '', serial: '', imeis: {data: ['', '']}, tipo: ''}, reparaciones: [{nombre: ''}], costo: 5.0, status: 'EN REPARACIÓN'}];
	let selectedDispositivoIndex = -1;
    let selectedDispositivo: any = null;
    let selectedTecnico = '';
    let nombres: any = '';
    let apellidos: any = '';
    let cedula: any = '';
    let telefono: any = '';
    let errors: any = {};
    let fecha_entrega: any = new Date();
    let fecha_salida: any = new Date();
    let cliente: any = '';
    let tecnico: any = ''; 
    let tipo: any = '1';
    let costototal: number = 0;
    let observaciones: any = '';
    $: total = dispositivos.reduce((acc, dispositivo: any) => acc + parseFloat(dispositivo.costo), 0);

    function addDispositivo() {
        dispositivos = [...dispositivos, {dispositivo: {marca: '', modelo: '', serial: '',  imeis: {data: ['', '']}, tipo: ''}, reparaciones: [{nombre: ''}], costo: 5.0, status: 'EN REPARACIÓN'}];
    }
    function removeDispositivo(dispositivo: any) {
        dispositivos = dispositivos.filter((d: any) => d !== dispositivo);
    }

    function removeReparacion(reparacion: any) {
        selectedDispositivoIndex = dispositivos.findIndex(dispositivo => dispositivo === selectedDispositivo);
        dispositivos[selectedDispositivoIndex].reparaciones = dispositivos[selectedDispositivoIndex]?.reparaciones.filter((r: any) => r !== reparacion);
        selectedDispositivo = dispositivos[selectedDispositivoIndex];
    }

    function addReparacion() {
        selectedDispositivoIndex = dispositivos.findIndex(dispositivo => dispositivo === selectedDispositivo);
        dispositivos[selectedDispositivoIndex].reparaciones= [...dispositivos[selectedDispositivoIndex].reparaciones, {nombre: ''}];
        selectedDispositivo = dispositivos[selectedDispositivoIndex];
    }

    function selectDispositivo(dispositivo: any) {
        selectedDispositivo = dispositivo;
    }
    function handleSubmit() {
        const endpoint = apiEndpoint + 'servicios' + '/' + data.id + '/';
        let cliente = {
            nombres: nombres,
            apellidos: apellidos,
            cedula: cedula,
            telefono: telefono
        };

        let servicio = {
            cliente: cliente,
            tecnico: tecnico,
            dispositivos: dispositivos,
            fecha_entrega: fecha_entrega,
            fecha_salida: fecha_salida,
            observaciones: observaciones
        }

        fetch(endpoint, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(servicio),
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

    $: showForm = false;
    onMount(async () => {
        await onlyAuthenticated();
        tecnicos = await getData(apiEndpoint + 'tecnicos');
        clientes = await getData(apiEndpoint + 'clientes');
        tiposDispositivos = await getData(apiEndpoint + 'tipos_dispositivos');
        tipo = tiposDispositivos[0]?.id;
        tecnico = tecnicos[0]?.id;

        let servicio = await getData(apiEndpoint + 'servicios/' + data.id + '/');
        dispositivos = servicio.dispositivos;
        dispositivos.map((dispositivo: any) => {
            if (dispositivo.dispositivo.imeis === null) {
                dispositivo.dispositivo.imeis = {data: ['', '']};
            }  
        });
        nombres = servicio.cliente.nombres;
        apellidos = servicio.cliente.apellidos;
        cedula = servicio.cliente.cedula;
        telefono = servicio.cliente.telefono;
        tecnico = servicio.tecnico;
        fecha_entrega = new Date(servicio.fecha_entrega).toISOString().split('T')[0]; // convert to ISO string and extract the date part only
        fecha_salida = new Date(servicio.fecha_salida).toISOString().split('T')[0]; // convert to ISO string and extract the date part only
        observaciones = servicio.observaciones;
        cliente = servicio.cliente.id;
        
    })
</script>

<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if !selectedDispositivo}
        <!-- PARTE 2-->
            <header class="flex justify-between items-center">
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Agregar Servicio</h1>
                
            </header>
            <form>
                <h2 class="h2 m-5 text-secondary-50 font-bold italic">Cliente</h2>
                <div class="w-[70%]">
                    <div class="flex flex-row">
                        <div class="mx-4 w-[50%]">
                            <label for="fecha_entrega" class="text-secondary-100 font-bold">Fecha de Entrada</label>
                            <input type="date" name="fecha_entrega" class="w-full" bind:value={fecha_entrega}>
                        </div>
                        <div class="mx-4  w-[50%]">
                            <label for="fecha_salida" class="text-secondary-100 font-bold">Fecha de Salida</label>
                            <input type="date" name="fecha_salida" class="w-full" bind:value={fecha_salida}>
                        </div>
                    </div>
                    <div class="flex flex-row">
                        <div class="mx-4 w-[50%]">
                            <label for="nombres" class="text-secondary-100 font-bold">Nombres</label>
                            <input type="text" name="nombres" class="w-full" bind:value={nombres}>
                        </div>
                        <div class="mx-4  w-[50%]">
                            <label for="apellidos" class="text-secondary-100 font-bold">Apellidos</label>
                            <input type="text" name="apellidos" class="w-full" bind:value={apellidos}>
                        </div>
                    </div>
                    
                    <div class="flex flex-row w-full">
                        <div class="mx-4 w-1/3">
                            <label for="cedula" class="text-secondary-100 font-bold">Cedula</label>
                            <input type="text" name="cedula" class="w-full" bind:value={cedula}>
                        </div>
                        <div class="mx-4 w-1/3" >
                            <label for="telefono" class="text-secondary-100 font-bold">Nro. Teléfono</label>
                            <input type="text" name="telefono" class="w-full" bind:value={telefono}>
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
                        <div class="mx-4 w-full">
                            <label for="observaciones" class="text-secondary-100 font-bold" >Observaciones</label>
                            <textarea name="observaciones" class="w-full" bind:value={observaciones}></textarea>
                        </div>
                    </div>
                </div>
                <h2 class="h2 m-5 text-secondary-50 font-bold italic">Dispositivos</h2>
                <div class="w-full m-4">
                    <table class="table table-hover table-compact w-full table-auto overflow-x-scroll">
                        <thead>
                            <tr>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Marca</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Modelo</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Serial</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Tipo</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Imei 1</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Imei 2</th>
                                <th class="variant-filled-tertiary border border-gray-100 font-bold text-center">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="variant-filled-secondary">
                            {#each dispositivos as dispositivoServicio}
                                <tr>
                                    <td class="border-gray-100 font-bold text-center">
                                        <input type="text" bind:value={dispositivoServicio.dispositivo.marca} class="w-[10rem]">
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <input type="text" bind:value={dispositivoServicio.dispositivo.modelo}>
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <input type="text" bind:value={dispositivoServicio.dispositivo.serial}>
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <select name="tipoDispositivo" id="" bind:value={dispositivoServicio.dispositivo.tipo}>
                                            {#each tiposDispositivos as tipo}
                                                <option value={tipo.id}>{tipo.nombre}</option>
                                            {/each}
                                        </select>
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <input type="text" bind:value={dispositivoServicio.dispositivo.imeis.data[0]}>
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <input type="text" bind:value={dispositivoServicio.dispositivo.imeis.data[1]}>
                                    </td>
                                    <td class="border-gray-100 font-bold text-center w-[10rem] flex flex-row">
                                        <button type="button" class="p-2 btn btn-md variant-filled-primary border border-gray-500" on:click={() => selectDispositivo(dispositivoServicio)}>Reparaciones</button>
                                        <button type="button" class="p-2 btn btn-md variant-filled-primary border border-gray-500" on:click={() => removeDispositivo(dispositivoServicio)}>X</button>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>  
                        <tfoot>
                            <tr>
                                <td>Total {total}$</td>
                            </tr>
                        </tfoot>
                    </table>
                    <button type="button" class="ml-4 font-bold text-5xl" on:click={addDispositivo}>
                        +
                    </button>
                </div>
                <div class="flex flex-row">
                    <button
                    type="button"
                    class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                    on:click={handleSubmit}
                    >Guardar</button>
                    <button
                    type="button"
                    class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
                    on:click={() => showForm = !showForm}
                    >Imprimir</button>
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
        {:else}
            <header class="flex justify-between items-center">
                {#if selectedDispositivo.marca !== ''} 
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Reparaciones de {selectedDispositivo?.dispositivo.marca} {selectedDispositivo?.dispositivo.modelo}</h1>
                {:else}
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Reparaciones</h1>
                {/if}
            </header>
            <div class="w-[45rem]">
                <table class="table table-hover table-compact table-auto overflow-x-scroll">
                    <thead>
                        <tr>
                            <th class="variant-filled-tertiary border border-gray-100 font-bold text-center w-full">Nombre</th>
                            <th class="variant-filled-tertiary border border-gray-100 font-bold text-center w-[2rem]">Acciones</th>
                        </tr>
                    </thead>
                    <tbody class="variant-filled-secondary">
                        {#each selectedDispositivo?.reparaciones as reparacion}
                            <tr>
                                <td class="border-gray-100 font-bold text-center">
                                    <input type="text" bind:value={reparacion.nombre} class="w-full">
                                </td>
                                
                                <td class="border-gray-100 font-bold text-center w-[2rem] flex flex-row">
                                   
                                    <button type="button" class="p-2 text-center btn btn-md variant-filled-primary border border-gray-500" on:click={() => removeReparacion(reparacion)}>X</button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>  
                </table>
                <div class="flex flex-col">
                    <button type="button" class="my-2 w-min font-bold text-5xl" on:click={addReparacion}>
                        +
                    </button>
                    <div class="flex flex-row">
                        <div class="flex flex-col my-2 mb-4 w-[10rem]">
                            <label for="" class="text-start w-full">Costo</label>
                            <input type="number" class="" min="5" step="0.01" bind:value={selectedDispositivo.costo}>
                        </div>
                        <div class="flex flex-col my-2 mb-4 w-[10rem] mx-4">
                            <label for="" class="text-start w-full">Status</label>
                            <select name="status" id="status" bind:value={selectedDispositivo.status} class="w-full">
                                <option value="EN REPARACIÓN">En reparación</option>
                                <option value="REPARADO">Reparado</option>
                        </div>
                    </div>
                    
                    <button
                            type="button"
                            class="btn btn-md variant-filled-primary w-min border border-gray-500"
                            on:click={() => selectDispositivo(null)}
                        >
                            <span>Volver</span>
                        </button>
                </div>
            </div>
        {/if}
    </div>
	
</div>