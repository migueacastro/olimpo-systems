<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { apiEndpoint } from '$lib/endpoint';
    initializeStores();
	
	let id: any = '';
	let cedula: any = '';
	let nombres: any = '';
	let apellidos: any = '';
	let telefono: any = '';

	$: showForm = false;

	let handleSubmit = () => {
        const endpoint = apiEndpoint + 'dispositivos/' ;
        let data = new FormData();
        data.append('marca', cedula);
        data.append('modelo', nombres);
        data.append('serial', apellidos);
        data.append('tipo', telefono);

        fetch(endpoint, {
            method: 'POST',
            body: data,
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
</script>

<div class="space-y-10">
	<!-- Header -->
	<div class="mx-5 lg:m-32">
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Técnicos</h1>
			<button
					type="button"
					class="btn btn-md variant-filled-primary border border-gray-500"
				>
					<span>Agregar</span>
				</button>
		</header>
		<!-- Component -->
		<Datatable endpoint="tecnicos" fields={['id', 'cedula', 'nombres', 'apellidos', 'telefono']} />
	</div>
	
</div>