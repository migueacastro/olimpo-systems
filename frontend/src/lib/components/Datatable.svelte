<script lang="ts">
	//Import local datatable components
	import ThSort from '$lib/components/ThSort.svelte';
	import ThFilter from '$lib/components/ThFilter.svelte';
	import Search from '$lib/components/Search.svelte';
	import RowsPerPage from '$lib/components/RowsPerPage.svelte';
	import RowCount from '$lib/components/RowCount.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { goto } from '$app/navigation';
	import { filter, getModalStore } from '@skeletonlabs/skeleton';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { getData } from '$lib/components/data';
	import { apiEndpoint } from '$lib/endpoint';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { user } from '$lib/stores/auth';
	import { check } from '@vincjo/datatables';
	

	//Import handler from SSD
	import { DataHandler, type Row } from '@vincjo/datatables';
	import { onMount } from 'svelte';

	export let endpoint: string = '';
	export let fields: string[] = [];

	function formatDispositivos(data: any) {
		console.log(modelos);
		console.log(marcas);
		console.log(data);
		return data.map((d: any) => {
			let marca = marcas.find((m: any) => m.id === d.dispositivo.marca);
			let modelo = modelos.find((m: any) => m.id === d.dispositivo.modelo);
			return marca.nombre + ' ' + modelo.nombre;
		}).join(', ');
	}
	let modelos: any = [];
	let marcas: any = [];
	let data: any = [{}];
	let tecnicos: any = [];
	let tecnico: any = '';
	let status : any;
	let desde: Date = new Date();
	let hasta: Date = new Date();
	let salida: boolean = false;
	let entrega: boolean = false;
	const modalStore = getModalStore();
	
	function capitalize(s: string) {
		if (typeof s !== 'string') {
			return '';
		}
		return s.charAt(0).toUpperCase() + s.slice(1);
	}
	function formatTitle(s: string) {
		return s.replace(/_/g, ' ');
	}
	function modalDelete(row: { name: string }) {
		modalStore.trigger({
			type: 'confirm',
			title: 'Delete ' + row.name,
			body: 'Are you sure you want to delete ' + row.name + '?',
			response: (r) => {
				if (r) {
					deleteRow(row);
				}
			}
		});
	}
	function deleteRow(row: any) {
		//TODO: Delete row
		fetch(apiEndpoint + endpoint + '/' + row.id, {
			method: 'DELETE',
		}).then((response) => {
			if (response.ok) {
				modalStore.close();
				toastStore.trigger({
					message: 'Deleted ' + row.name,
					background: 'variant-filled-warning'
				});
				getData(apiEndpoint + endpoint).then((data) => {
					handler = new DataHandler(data, { rowsPerPage: 5 });
					rows = handler.getRows();
				});
			} else {
				window.location.reload();
			}
		});
	}

	function editRow(row: any) {
		goto('/' + endpoint + '/' + row.id);
	}


	
	const toastStore = getToastStore();
	const endpointName = endpoint.split('/').slice(-1)[0];

	let handler = new DataHandler(data, { rowsPerPage: 5 });
	/*
	const fechaEntregaFilter = handler.createAdvancedFilter('fecha_entrega'); 
	const fechaSalidaFilter = handler.createAdvancedFilter('fecha_salida'); 
	const selectedFechaEntrega = fechaEntregaFilter.getSelected(); 
	const selectedFechaSalida = fechaSalidaFilter.getSelected();
	function handleDateFilter() { 
		const desdeTimestamp = desde ? new Date(desde).getTime() : new Date('1970-01-01').getTime(); 
		const hastaTimestamp = hasta ? new Date(hasta).getTime() : new Date('9999-12-31').getTime(); 
		if (entrega) { 
			fechaEntregaFilter.set([desdeTimestamp, hastaTimestamp], check.isBetween); 
		} else if (salida) { 
			fechaSalidaFilter.set([desdeTimestamp,hastaTimestamp], check.isBetween); 
		} else { 
			fechaSalidaFilter.clear(); // Clear filter if not applied 
			fechaEntregaFilter.clear();
		}
	} 
	*/
	const fechaEntregaFilter = handler.createAdvancedFilter('fecha_entrega'); 
	const fechaSalidaFilter = handler.createAdvancedFilter('fecha_salida');
	function convertDMYToTimestamp(dmy: string): number { 
		const [day, month, year] = dmy.split('/').map(Number); 
		return new Date(year, month - 1, day).getTime(); 
	}
	function dateRangeComparator(entry: string, filter: { desde: number; hasta: number }) { 
		const entryTimestamp = convertDMYToTimestamp(entry); 
		const { desde, hasta } = filter; 
		return entryTimestamp >= desde && entryTimestamp <= hasta; 
	} 

	 // Function to handle date filter change 
	function handleDateFilter() { 
		const desdeTimestamp = desde ? new Date(desde).getTime() : new Date('1970-01-01').getTime(); 
		const hastaTimestamp = hasta ? new Date(hasta).getTime() : new Date('9999-12-31').getTime(); 
		const filterValues = { desde: desdeTimestamp, hasta: hastaTimestamp }; 
		handler.clearFilters();
		if (entrega) { 
			handler.filter(filterValues, 'fecha_entrega', (entry, filter) => dateRangeComparator(entry, filter)); 
		} else { 
			fechaEntregaFilter.clear(); // Clear filter if not applied 
		} if (salida) { 
			handler.filter(filterValues, 'fecha_salida', (entry, filter) => dateRangeComparator(entry, filter)); 
		} else { 
			fechaSalidaFilter.clear(); // Clear filter if not applied 
		} 
		handler.setRows(data);
	}
	$: handleDateFilter();
	$: rows = handler.getRows();

	onMount(async () => {
		if (endpoint === 'servicios') {
			tecnicos = await getData(apiEndpoint + 'tecnicos');
		}
		marcas = await getData(apiEndpoint + 'marcas');
		modelos = await getData(apiEndpoint + 'modelos');	
		data = await getData(apiEndpoint + endpoint);
		handler = new DataHandler(data, { rowsPerPage: 5 });
		rows = handler.getRows();
		
	});
</script>

<div class=" overflow-x-auto space-y-4">

	<!-- Header -->
	<header class="flex justify-between gap-4 flex-row">
		<div class="flex flex-row">
			<div class="flex flex-col">
				<label for="status" class="text-white font-bold">Buscar</label>
				<Search {handler} />
			</div>	
		</div>	
		
		{#if endpoint === 'servicios'}
		<div class="flex flex-col">
			<label for="desde" class="text-white font-bold">Desde</label>
			<input type="date" bind:value={desde} on:input={handleDateFilter}>
		</div>	
		<div class="flex flex-col">
			<label for="hasta" class="text-white font-bold">Hasta</label>
			<input type="date" bind:value={hasta} on:input={handleDateFilter}>
		</div>	
		<div class="flex flex-col">
			<label for="hasta" class="text-white font-bold">Fechas de</label>
			<div class="flex flex-row align-bottom p-2">
				<p class="mx-2 text-white font-bold"><input type="checkbox" name="" id="" class="mx-1" bind:checked={entrega} on:change={handleDateFilter}>Entrega</p>
				<p class="mx-2 text-white font-bold"><input type="checkbox" name="" id="" class="mx-1" bind:checked={salida} on:change={handleDateFilter}>Salida</p>
			</div>
		</div>	
		<div class="flex flex-row mx-2">
			<div class="flex flex-col">
				<label for="tecnico" class="text-white font-bold">Técnico</label>
				<select name="tecnico" id="" bind:value={tecnico} on:change={() => handler.filter(tecnico, 'nombre_tecnico')}>
					<option value=""></option>
					{#each tecnicos as tecnico}
						<option value={tecnico.nombres + ' ' + tecnico.apellidos}>{tecnico.nombres} {tecnico.apellidos}</option>
					{/each}
				</select>
			</div>	
		</div>	
		<div class="flex flex-row">
			<div class="flex flex-col">
				<label for="status" class="text-white font-bold">Status</label>
				<select name="status" id="" bind:value={status} on:change={() => handler.filter(status, 'status')}>
					<option value=""></option>
					<option value="{"REPARADO"}">{"Reparado"}</option>
					<option value="{"EN REPARACIÓN"}">{"En Reparación"}</option>	
				</select>
			</div>	
		</div>		
		{/if}
	</header>
	<!-- Table -->
	{#if data[0]?.id && data.length > 0 || data.length === 0}
		<table class="table table-hover table-compact w-full table-auto">
			<thead>
				<tr>
					{#each fields as field}
						<ThSort {handler} orderBy={field}
							>{field.replace(/_name/g, ' ').replace(/_/g, ' ')}</ThSort
						>
					{/each}
					{#if (endpoint === 'tecnicos' && $user.is_superuser) || endpoint != 'tecnicos'}
					<td class="variant-filled-tertiary border border-gray-100 font-bold text-center"
						>Acciones</td
					>
					{/if}
				</tr>
			</thead>
			<tbody class="variant-filled-secondary">
				{#each $rows as row}
					<tr>
						{#each fields as field}
						<td class="texrt-justify indent-2 text-wrap border border-gray-500">
							{#if typeof row[field] === 'object'}
								{#if row[field]?.data}
									{#if  row[field].data[0] === "" && row[field].data[1] === ""}
										{"No"}
									{:else }
										{row[field]?.data.join(', ')}
									{/if}
								{:else if row[field]?.length  && row[field]?.[0]?.dispositivo}
									{formatDispositivos(row[field])}
								{:else if row[field] == null}
									{"No"}
								{:else}					
									{(row[field]?.nombre) ? row[field]?.nombre : row[field]?.nombres}
								{/if}
							{:else }
								{row[field]}
							{/if}
						</td>
						{/each}
						{#if (endpoint === 'tecnicos' && $user.is_superuser) || endpoint != 'tecnicos'}
						<td class="flex flex-row gap-3 mx-2">
							<button
								on:click|stopPropagation={() => deleteRow(row)}
								class="btn variant-filled-primary border border-gray-500 w-1/2 h-[2rem]"
								>Eliminar
							</button>|
							<button
								on:click|stopPropagation={() => editRow(row)}
								class="btn variant-filled-primary border border-gray-500 w-1/2 h-[2rem]"
								>Editar</button
							>
						</td>
						{/if}
					</tr>
				{/each}
			</tbody>
		</table>
		<!-- Footer -->
		<footer class="flex justify-between">
			<RowCount {handler} />
			<Pagination {handler} />
		</footer>
	{:else}
		<div class="flex flex-row justify-center">
			<ProgressRadial value={undefined} />
		</div>
	{/if}
</div>
