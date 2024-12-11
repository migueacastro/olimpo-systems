import { goto } from "$app/navigation";
import { env } from "$env/dynamic/public";
import { writable } from 'svelte/store';
import type { Writable } from "svelte/store"; 
import { apiEndpoint } from "$lib/endpoint";


interface User {
    nombres: any;
    apellidos: any;
    cedula: any;
    email: any;
    is_superuser: any;
    is_staff: any;
}
export const user: Writable<User> = writable({nombres: null, apellidos: null, cedula: null, email: null, is_superuser: null, is_staff:null})
export const authenticated = writable(false);
export const userInitials = writable('');

// In case a page needs authorization, put our little friend in onMount() :)
export const onlyAuthenticated = async () => {
    try {
        const response = await fetch(`${apiEndpoint}user`, {
            headers: {'Content-Type': 'application/json'},
            credentials: 'include'
        });
        if (response.ok) {
            const data = await response.json();
			await setAuthData(data); // In case it retrieves the user info, just set it true
            return true;
        } else {
            await goto('/login'); // Otherwise, set it to false
            return false;
        }
    } catch (error) {
        await goto('/login');
        return false;
    }
}


// In case a page needs you to be Staff, put our little friend in onMount() :)
export const onlyStaff = async (userData: any) => {
    await authenticateUser();
    await onlyAuthenticated();
    if (!userData.is_staff) {
        await goto('/login');
    }
}


// In case a page needs you to be Admin, put our little friend in onMount() :)
export const onlyAdmin = async (userData: any) => {
    await authenticateUser();
    await onlyAuthenticated();
    if (!(userData.is_superuser) || !await onlyAuthenticated()) {
        await window.history.back();
    }
}

function deleteCookie(name: any) { 
    document.cookie = name + '=; Max-Age=0; path=/; domain=' + window.location.hostname; 
}
export const authenticateUser = async () => {
    try {
        const response = await fetch(`${apiEndpoint}user`, {
            headers: {'Content-Type': 'application/json'},
            credentials: 'include'
        });
        if (response.ok) {
            const data = await response.json();
			setAuthData(data); // In case it retrieves the user info, just set it true
        } else {
            unauthenticateUser(); // Otherwise, set it to false
        }
    } catch (error) {
        unauthenticateUser();
    }
}

// Use the serializers data and put it inside of user object
export const setAuthData = (value: any) => {
    user.set(value);
    authenticated.set(true);
}

export const unauthenticateUser = async () => {
    const response = await fetch(`${apiEndpoint}logout`, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include' 
    });
    if (response.ok) {
        user.set({nombres: null, apellidos: null, cedula: null, email: null, is_staff: false, is_superuser: false})
        document.cookie = 'access_token=; Max-Age=0; path=/; domain=127.0.0.1;';
        authenticated.set(false);
        goto('/login');
        
    } else {
        console.log('Error logging out');
    }
    
}