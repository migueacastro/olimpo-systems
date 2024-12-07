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

    interface Dispositivo {
        marca: any | null;
		modelo: any | null;
		serial: string | null;
		imeis: any;
		tipo: string | null;
        modelos_marca: any;
    }
    interface DispositivoServicio {
		dispositivo: any;
        reparaciones: any;
        costo: number | null;
        status: string | null;
	}
	let dispositivos: Array<DispositivoServicio> = [{dispositivo: {modelos_marca: [], marca: '', modelo: '', serial: '', imeis: {data: ['', '']}, tipo: ''}, reparaciones: [{nombre: 'Revisión'}], costo: 5.0, status: 'EN REPARACIÓN'}];
	let selectedDispositivoIndex = -1;
    let selectedDispositivo: any = null;
    let selectedTecnico = '';
    let nombres: any = '';
    let apellidos: any = '';
    let cedula: any = '';
    let telefono: any = '';
    let errors: any = {};
    let fecha_entrega = new Date();
    let fecha_salida = new Date();
    let cliente: any = '';
    let tecnico: any = ''; 
    let tipo: any = '1';
    let marcas: any = [];
    let servicios = [];

    let modelos: any = [];

    let observaciones: any = '';
    let total = dispositivos.reduce((acc, dispositivo: any) => acc + parseFloat(dispositivo.costo), 0);

    function filterModelos(marca: any) {
        return marcas.find((m: any) => m.id === marca)?.modelos || [];
    }
    function updateDispositivos() {
        total = dispositivos.reduce((acc, dispositivo: any) => acc + parseFloat(dispositivo.costo), 0);
    }
    function addDispositivo() {
        dispositivos = [...dispositivos, {dispositivo: {marca: '', modelo: '', serial: '', imeis: {data: ['', '']}, tipo: ''}, reparaciones: [{nombre: 'Revisión'}], costo: 5.0, status: 'EN REPARACIÓN'}];
        updateDispositivos();
    }
    function removeDispositivo(dispositivo: any) {
        dispositivos = dispositivos.filter((d: any) => d !== dispositivo);
        updateDispositivos();
    }

    function findMarcaById(id: any) {
        return marcas.find((m: any) => m.id === id);
    }

    function findModeloById(id: any) {
        return modelos.find((m: any) => m.id === id);
    }

    function removeReparacion(reparacion: any) {
        selectedDispositivoIndex = dispositivos.findIndex(dispositivo => dispositivo === selectedDispositivo);
        dispositivos[selectedDispositivoIndex].reparaciones = dispositivos[selectedDispositivoIndex]?.reparaciones.filter((r: any) => r !== reparacion);
        selectedDispositivo = dispositivos[selectedDispositivoIndex];
        updateDispositivos();
    }

    function addReparacion() {
        selectedDispositivoIndex = dispositivos.findIndex(dispositivo => dispositivo === selectedDispositivo);
        dispositivos[selectedDispositivoIndex].reparaciones= [...dispositivos[selectedDispositivoIndex].reparaciones, {nombre: ''}];
        selectedDispositivo = dispositivos[selectedDispositivoIndex];
        updateDispositivos();
    }

    function selectDispositivo(dispositivo: any) {
        selectedDispositivo = dispositivo;
        selectedDispositivoIndex = dispositivos.findIndex(dispositivo => dispositivo === selectedDispositivo);
    }
    function handleSubmit() {
        const endpoint = apiEndpoint + 'servicios' + '/';
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
            method: 'POST',
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

    function parseDate(dateStr: string) { 
        let [day, month, year] = dateStr.split('/'); 
        return new Date(`${year}-${month}-${day}`).toISOString().split('T')[0]; 
    }

    $: showForm = false;
    onMount(async () => {
        await onlyAuthenticated();
        tecnicos = await getData(apiEndpoint + 'tecnicos');
        clientes = await getData(apiEndpoint + 'clientes');
        tiposDispositivos = await getData(apiEndpoint + 'tipos_dispositivos');
        tipo = tiposDispositivos[0]?.id;
        tecnico = tecnicos[0]?.id;
        marcas = await getData(apiEndpoint + 'marcas');
        modelos = await getData(apiEndpoint + 'modelos');
        servicios = await getData(apiEndpoint + 'servicios');
        
        
    })
</script>

<div class="space-y-10 h-full">
   
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
        <!-- PARTE 1 -->
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Servicios: {servicios?.length}</h1>
			<button
				type="button"
				class="btn btn-md variant-filled-primary border border-gray-500"
				on:click={() => showForm = !showForm}
			>
				<span>Agregar</span>
            </button>
		</header>
		<Datatable endpoint="servicios" fields={['id', 'fecha_entrega', 'fecha_salida', 'nombre_tecnico', 'nombre_cliente', 'cedula', 'dispositivos', 'costo_total', 'status']} />
        <!-- FIN PARTE 1 -->
        {:else if !selectedDispositivo}
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
                            <input type="text" name="cedula" class="w-full" bind:value={cedula} on:input={() => findClientByCedula(cedula)}>
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
                            {#each dispositivos as dispositivoServicio, index (dispositivoServicio.dispositivo.serial)}
                                
                                <tr>
                                    <td class="border-gray-100 font-bold text-center">
                                        <select name="marca" id="marca" bind:value={dispositivoServicio.dispositivo.marca} class="w-full">
                                            {#each marcas as marca}
                                                <option value={marca.id}>{marca.nombre}</option>
                                            {/each}
                                        </select>     
                                    </td>
                                    <td class="border-gray-100 font-bold text-center">
                                        <select name="modelo" id="modelo" bind:value={dispositivoServicio.dispositivo.modelo} class="w-full">
                                            {#each filterModelos(dispositivoServicio.dispositivo.marca) as modelo}
                                                <option value={modelo.id}>{modelo.nombre}</option>
                                            {/each}
                                        </select>     
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
                <h1 class="h1 m-5 text-secondary-50 font-bold italic">Reparaciones de {findMarcaById(selectedDispositivo?.dispositivo.marca).nombre} {findModeloById(selectedDispositivo?.dispositivo.modelo).nombre}</h1>
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
                        {#each dispositivos[selectedDispositivoIndex].reparaciones as reparacion}
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
                            <input type="number" class="" min="5" step="0.01" bind:value={selectedDispositivo.costo}  on:input={updateDispositivos}>
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