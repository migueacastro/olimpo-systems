<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
	
</script>

<div class="space-y-10">
	<!-- Header -->
	<div class="m-32">
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5">Técnicos</h1>
			<a
				type="button"
				class="btn btn-sm variant-filled rounded-md"
				href="#"
				target="_blank"
			>
				<span>Agregar</span>
			</a>
		</header>
		<!-- Divider -->
		<hr class="m-5"/>
		<!-- Component -->
		<Datatable endpoint="tecnicos" fields={['id', 'cedula', 'nombres', 'apellidos', 'telefono']} />
	</div>
	
</div>