<script lang="ts">
	import Datatable from '$lib/components/Datatable.svelte';
    import { initializeStores } from '@skeletonlabs/skeleton';
	import { apiEndpoint } from '$lib/endpoint';
    initializeStores();
    import { getModalStore } from '@skeletonlabs/skeleton';
	
	let id: any = '';
	let cedula: any = '';
	let nombres: any = '';
	let apellidos: any = '';
	let telefono: any = '';

	$: showForm = false;

	function handleSubmit() {
        const endpoint = apiEndpoint + 'tecnicos' + '/';
        let data = new FormData();
        data.append('cedula', cedula);
        data.append('nombres', nombres);
        data.append('apellidos', apellidos);
        data.append('telefono', telefono);

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
    }
</script>

<div class="space-y-10">
	<!-- Header -->
	<div class="mx-5 lg:m-32">
        {#if showForm === false}
		<header class="flex justify-between items-center">
			<h1 class="h1 m-5 text-secondary-50 font-bold italic">Técnicos</h1>
			<button
                    on:click={() => showForm = !showForm}
					type="button"
					class="btn btn-md variant-filled-primary border border-gray-500"
				>
				
                <span>Agregar</span>
				</button>

		</header>
		<!-- Component -->
		<Datatable endpoint="tecnicos" fields={['id', 'cedula', 'nombres', 'apellidos', 'telefono']} />
        {:else}
        <form>
            <div class="w-[70%]">
                
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4  w-1/3">
                        <label for="nombres" class="text-secondary-100 font-bold">Nombres</label>
                        <input type="text" name="nombres" class="w-full" bind:value={nombres}>
                    </div>
                    <div class="mx-4  w-1/3">
                        <label for="apellidos" class="text-secondary-100 font-bold">Apellidos</label>
                        <input type="text" name="apellidos" class="w-full" bind:value={apellidos}>
                    </div>
                </div>
                <div class="flex flex-row w-full">
                    
                    <div class="mx-4  w-1/3">
                        <label for="cedula" class="text-secondary-100 font-bold">Cedula</label>
                        <input type="text" name="cedula" class="w-full" bind:value={cedula}>
                    </div>
                    <div class="mx-4  w-1/3">
                        <label for="telefono" class="text-secondary-100 font-bold">Teléfono</label>
                        <input type="text" name="telefono" class="w-full" bind:value={telefono}>
                    </div>
                </div>
            </div>
            <button
            type="button"
            class=" m-4 btn btn-md variant-filled-primary border border-gray-500"
            on:click={handleSubmit}
            >Guardar</button>       
        </form>
        {/if}
	</div>
	
</div>