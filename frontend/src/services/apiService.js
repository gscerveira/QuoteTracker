import axios from 'axios';
import Cookies from 'js-cookie';


const API_URL = process.env.REACT_APP_API_URL;

const getCsrfToken = () => {
    return Cookies.get('csrftoken');
};

const register = (username, email, password) => {
    return axios.post(API_URL + 'register/', {
        username,
        email,
        password
    });
};

const login = (username, password) => {
    return axios.post(API_URL + 'login/', {
        username,
        password
    }, {
        headers: { 'X-CSRFToken': getCsrfToken() },
        withCredentials: true
    });
};

// Logout
const logout = async () => {
    try {
        await axios.post(API_URL + 'logout/', {}, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
    } catch (error) {
        console.error('Error logging out:', error);
        throw error;
    }
};

const fetchProjects = async () => {
    try {
        const response = await axios.get(API_URL + 'projects/', {
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching projects:', error);
        throw error;
    }
};

const createProject = async (projectData) => {
    try {
        const response = await axios.post(API_URL + 'projects/', projectData, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error creating project:', error);
        throw error;
    }
};

const updateProject = async (projectId, projectData) => {
    try {
        const response = await axios.patch(API_URL + `projects/${projectId}/`, projectData, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error updating project:', error);
        throw error;
    }
};

const deleteProject = async (projectId) => {
    try {
        const response = await axios.delete(API_URL + `projects/${projectId}/`, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error deleting project:', error);
        throw error;
    }
};

const fetchItems = async (projectId) => {
    try {
        const response = await axios.get(API_URL + 'items/?project=', projectId, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching items:', error);
        throw error;
    }
};

const createItem = async (itemData) => {
    try {
        const response = await axios.post(API_URL + 'items/', itemData, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error creating item:', error);
        throw error;
    }
};

const updateItem = async (itemId, itemData) => {
    try {
        const response = await axios.patch(API_URL + `items/${itemId}/`, itemData, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error updating item:', error);
        throw error;
    }
};

const deleteItem = async (itemId) => {
    try {
        const response = await axios.delete(API_URL + `items/${itemId}/`, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error deleting item:', error);
        throw error;
    }
};


// Get all stores
const fetchStores = async () => {
    try {
        const response = await axios.get(API_URL + 'stores/', { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching stores:', error);
        throw error;
    }
};

// Get store by id
const fetchStore = async (storeId) => {
    try {
        const response = await axios.get(API_URL + `stores/${storeId}/`, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching store:', error);
        throw error;
    }
};

const createStore = async (storeData) => {
    try {
        const response = await axios.post(API_URL + 'stores/', storeData, {
            headers: { 'X-CSRFToken': getCsrfToken() },
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        console.error('Error creating store:', error);
        throw error;
    }
};

export { register, login, logout, fetchProjects, createProject, fetchItems, createItem, updateItem, updateProject, deleteProject, deleteItem, fetchStores, fetchStore, createStore };