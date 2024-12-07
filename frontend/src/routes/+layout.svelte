<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';
	import { authenticateUser, user, onlyAuthenticated, unauthenticateUser } from '$lib/stores/auth';
	import { goto } from '$app/navigation';	
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';

	import { initializeStores } from '@skeletonlabs/skeleton';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);
	initializeStores();
	// Floating UI for Popups
	let isLoading = true;
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	onMount(async () => {
		await authenticateUser();
		await onlyAuthenticated();
		isLoading = false;
	})
	
	let url = $page.url.pathname;
	let currentPage = url.split("/").pop();
	console.log(currentPage);
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar background="variant-filled-tertiary">
			<svelte:fragment slot="lead">
				<a href="/"><strong class="text-xl uppercase font-bold italic">Olimpo Systems</strong></a>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if $user.email !== null}
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => goto('/servicios')}
				>
					Servicios
				</button>
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => goto('/clientes')}
				>
					Clientes
				</button>
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => goto('/dispositivos')}
				>
					Dispositivos
				</button>
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => goto('/modelos')}
				>
					Modelos
				</button>
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => goto('/marcas')}
				>
					Marcas
				</button>
				{#if $user.is_superuser}
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={() => window.location.href = '/tecnicos'}
				>
					Técnicos
				</button>
				{/if}
				<p
					class=" variant-fill-surface font-bold"
				>
					{$user.nombres + ' ' + $user.apellidos} | {($user.is_superuser) ? 'Administrador' : 'Tecnico'}
				</p>
				<button
					class="btn btn-sm variant-fill-surface font-bold"
					on:click={unauthenticateUser}
				>
					Cerrar Sesión
				</button>
			{/if}
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	{#if !isLoading}
	<slot/>
	{:else}
	<div class="flex flex-row justify-center pt-[10rem]">
		<ProgressRadial value={undefined} />
	</div>
	{/if}
</AppShell>
