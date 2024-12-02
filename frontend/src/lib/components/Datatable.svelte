<script lang="ts">
	//Import local datatable components
	import ThSort from '$lib/components/ThSort.svelte';
	import ThFilter from '$lib/components/ThFilter.svelte';
	import Search from '$lib/components/Search.svelte';
	import RowsPerPage from '$lib/components/RowsPerPage.svelte';
	import RowCount from '$lib/components/RowCount.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { goto } from '$app/navigation';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { getData } from '$lib/components/data';
	import { apiEndpoint } from '$lib/endpoint';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { user } from '$lib/stores/auth';

	//Import handler from SSD
	import { DataHandler } from '@vincjo/datatables';
	import { onMount } from 'svelte';
	export let endpoint: string = '';
	export let fields: string[] = [];

	function formatDispositivos(data: any) {
		return data.map((d: any) => {
			return d.dispositivo.marca + ' ' + d.dispositivo.modelo;
		}).join(', ');
	}

	let data: any = [{}];
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
	//Init data handler - CLIENT
	let handler = new DataHandler(data, { rowsPerPage: 5 });
	$: rows = handler.getRows();

	onMount(async () => {
		data = await getData(apiEndpoint + endpoint);
		handler = new DataHandler(data, { rowsPerPage: 5 });
		rows = handler.getRows();
	});
</script>

<div class=" overflow-x-auto space-y-4">
	<!-- Header -->
	<header class="flex justify-between gap-4">
		<Search {handler} />
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
