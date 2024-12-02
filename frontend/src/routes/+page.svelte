

<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { getData } from '$lib/components/data';
	import { apiEndpoint } from '$lib/endpoint';
	import { onlyAuthenticated } from '$lib/stores/auth';
	let servicios: any = [];
	let clientes: any = [];
	let tecnicos: any = [];

	let serviciosPorReparar = 0;
	let clientesActivos = 0;
	let tecnicosActivos = 0;
	let acumuladoMensual = 0;

	onMount(async () => {
		await onlyAuthenticated();

		servicios = await getData(apiEndpoint + 'servicios');
		clientes = await getData(apiEndpoint + 'clientes');
		tecnicos = await getData(apiEndpoint + 'tecnicos');

		serviciosPorReparar = servicios.filter((servicio: any) => servicio.status === 'EN REPARACIÓN').length;
		clientesActivos = clientes.length;
		tecnicosActivos = tecnicos.length;
		acumuladoMensual = servicios.reduce((total: any, servicio: any) => total + parseFloat(servicio.costo_total), 0);

	})
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h1 font-bold text-6xl text-white italic ">OLIMPO SYSTEMS</h2>
		<h4 class="h4 font-bold text-3xl text-white mb-10">Bienvenido</h4>
		<div class="grid grid-cols-4 ">
			
			<div class="text-white font-bold text-xl card variant-filled-tertiary p-5 m-4">
				Servicios por reparar: 
				<p class="text-4xl text-white font-bold">
					{serviciosPorReparar}
				</p>
			</div>
			<div class="text-white font-bold text-xl card variant-filled-tertiary p-5 m-4">
				Ingreso este mes: 
				<p class="text-4xl text-white font-bold">{acumuladoMensual}$</p>
			</div>
			<div class="text-white font-bold text-xl card variant-filled-tertiary p-5 m-4">
				Clientes:
				<p class="text-4xl text-white font-bold">{clientesActivos}</p> 
			</div>
			<div class="text-white font-bold text-xl card variant-filled-tertiary p-5 m-4">
				Tecnicos: 
				<p class="text-4xl text-white font-bold">
					{tecnicosActivos}
				</p>
			</div>
		</div>
	</div>
</div>
