

<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { getData } from '$lib/components/data';
	import { apiEndpoint } from '$lib/endpoint';
	import { onlyAuthenticated } from '$lib/stores/auth';
	import image from '$lib/images/fondo.jpeg';


	onMount(async () => {
		await onlyAuthenticated();
	})
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h1 font-bold text-6xl text-white italic ">OLIMPO SYSTEMS</h2>
		<h4 class="h4 font-bold text-3xl text-white mb-10">Bienvenido</h4>
		<img class="object-contain h-[30rem] w-auto rounded-xl" src={image} alt="Logo Olimpo">
	</div>
</div>
