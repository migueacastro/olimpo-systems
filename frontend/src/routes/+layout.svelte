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
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	onMount(async () => {
		await authenticateUser();
		await onlyAuthenticated();
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
				<strong class="text-xl uppercase font-bold italic">Olimpo Systems</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if $user.email !== null}
				<a
					class="btn btn-sm variant-fill-surface font-bold"
					href="/servicios"
				>
					Servicios
				</a>
				<a
					class="btn btn-sm variant-fill-surface font-bold"
					href="/clientes"
				>
					Clientes
				</a>
				<a
					class="btn btn-sm variant-fill-surface font-bold"
					href="/dispositivos" 
				>
					Dispositivos
				</a>
				{#if $user.is_superuser}
				<a
					class="btn btn-sm variant-fill-surface font-bold"
					href="/tecnicos" 
				>
					Técnicos
				</a>
				{/if}
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
	{#if $user.email !== null || currentPage == 'login'}
	<slot/>
	{:else}
	<div class="flex flex-row justify-center pt-[10rem]">
		<ProgressRadial value={undefined} />
	</div>
	{/if}
</AppShell>
