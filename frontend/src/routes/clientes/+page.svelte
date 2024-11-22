<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
	
</script>

<div class="space-y-10">
	<!-- Header -->
	<div class="mx-5 lg:m-32">
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Clientes</h1>
			<button
					type="button"
					class="btn btn-md variant-filled-primary border border-gray-500"
	
				>
					<span>Agregar</span>
				</button>
		</header>
		<!-- Component -->
		<Datatable endpoint="clientes" fields={['id', 'cedula', 'nombres', 'apellidos', 'telefono']} />
	</div>
	
</div>