import type { Writable } from "svelte/store";
import { writable } from "svelte/store"

interface FieldStorage {
    type: any;
    value: any;
    name: any;
    table: any;
    disabled:any
}
export const _fieldsStorage: Writable<FieldStorage[]> = writable([{type: null, value: null, name: null, table: null, disabled: null}]);