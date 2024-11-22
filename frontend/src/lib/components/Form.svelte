<script lang="ts">
    import { goto } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { FileDropzone, SlideToggle, Autocomplete, InputChip } from '@skeletonlabs/skeleton';
    import { popup } from '@skeletonlabs/skeleton';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { page } from '$app/stores';
    import { _fieldsStorage } from '../stores/form';
    import { apiEndpoint } from '$lib/endpoint';
    import { env } from '$env/dynamic/public';
    export let name = '';

    interface Field {
        type: string;
        value: string;
        name: string;
        table: string;
        disabled:boolean;
        hidden: boolean;

    }
    export let fields: Field[] = [{type: '', value: '', name: '', hidden: false, table: '', disabled: false}];
    export let endpointName = '';
    export let edit = false;
    let id = $page.params.id;
    
    let capitalizedName = name.charAt(0).toUpperCase() + name.slice(1);
    let tables: { [key: string]: any } = {};
    const toastStore = getToastStore();


    let manyToManyListsDict: Record<string, any> = {};
    let inputChipListsDict: Record<string, any> = {};
    let valueChipListsDict: Record<string, any> = {};
    let inputChipDict: Record<string, any> = {};

    let removedOptions = {};

    const loadEditValues = async () => {
        const response = await fetch(`${apiEndpoint}/${endpointName}/${id}/`, {
            credentials: 'include'
        });
        const data = await response.json();
        return data
    }
    
    const loadCreateForm = async () => {
        
        let data: any;
        if (edit) {
            data = await loadEditValues();
        }

        for await (let field of fields) {
            if (field.type === 'foreignKey' || field.type === 'manyToMany') {
                let table: any = await fetch(`${apiEndpoint}/${field.table}/`, {
                    credentials: 'include'
                });

                table = await table.json();
                tables[field.table] = table;

            } 

            if (edit) {
                field.value = data[field.name];
            }
        };
        _fieldsStorage.set(fields);
    }

    const toastSuccessSettings = {
        message: `${capitalizedName} added successfully`,
        background: 'variant-filled-success',
    };

    let validFields = () => {
        $_fieldsStorage.forEach((field: any) => {
            switch (field?.type) {
                case 'text':
                    if (field.length < 1) return false;
                    break;
                case 'date':
                    if (field.length < 1) return false;
                    break;
                case 'textarea':
                    if (field.length < 1) return false;
                    break;
                case 'integer':
                    if (field < 1) return false;
                    break;
                case 'decimal':
                    if (field < 1) return false;
                    break;
                case 'boolean':
                    if (field === null) return false;
                    break;
                case 'foreignKey':
                    if (!field.value) return false;
                    break;
                default:
                    return true;
            }
        })
        return false;
    }

    const showInvalidMessage = (message: string) => {
        toastStore.trigger({
            message,
            background: 'variant-filled-error',
        });
    }
    
    const handleSubmit = async () => {
        
        if (validFields()) {
            showInvalidMessage('All fields are required');
            return;
        }
        
        const formData = new FormData();
    };


    onMount(async () => {
        
        await loadCreateForm();
        
        
        
    });
</script>

<div class="animate-show">
    <h2 class="h1 text-start mb-4">{edit ? 'Edit' : 'Add'} {capitalizedName}</h2>
    
    <form class=" gap-10 flex flex-col lg:flex-row" on:submit={handleSubmit}>
        <div class="card my-3 p-10 text-start lg:w-[75%] space-y-6">
            {#each $_fieldsStorage as field}
                <label class="label" for="{(field?.type == 'object') ? 'file' : field?.name }" class:hidden={field?.type === 'hidden'}>
                    <p class="capitalize">{field?.name?.replace(/_name/g, ' ').replace(/_/g, ' ')}</p>
                    {#if field?.type === 'text'}
                        <input class="input" type="text" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'password'}
                        <input class="input" type="password" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'decimal'}
                        <input class="input w-[25%]" type="number" placeholder="" min="0" step="0.01" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'integer'}
                        <input class="input w-[25%]" type="number" placeholder="" min="0" bind:value={field.value} id="{field.name}" disabled={field?.disabled}/>
                    {:else if field?.type === 'boolean'}
                        <SlideToggle name={field.name} bind:checked={field.value} id="toggle-{field.name}"/>
                    {:else if field?.type === 'hidden'}
                        <input class="input" type="hidden" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'date'}
                        <input class="input" type="date" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'datetime'}
                        <input class="input" type="datetime-local" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type === 'textarea'}
                        <textarea class="textarea" rows="4" placeholder="" bind:value={field.value} id="{field.name}"/>
                    {:else if field?.type == 'foreignKey'}
                       
                        {#if tables && tables[field.table]}
                        <select class="select" bind:value={field.value} id="{field.name}">
                            {#each tables[field.table] as option}
                                <option value={option.id}>{option.name}</option>
                            {/each}
                        </select>     
                        {/if}
                    {/if}
                </label>
            {/each}
            <button type="submit" class="btn variant-filled h-fit w-fit mx-auto btn-xl">Save</button>
        </div>    
    </form>
</div>