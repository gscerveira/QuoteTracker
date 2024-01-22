import axios from 'axios';

const API_URL = 'http://localhost:8000/tracker_app/';

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
    });
};

const fetchProjects = async () => {
    try {
        const response = await axios.get(API_URL + 'projects-list/');
        return response.data;
    } catch (error) {
        console.error('Error fetching projects:', error);
        throw error;
    }
};

const createProject = async (projectData) => {
    try {
        const response = await axios.post(API_URL + 'projects/', projectData);
        return response.data;
    } catch (error) {
        console.error('Error creating project:', error);
        throw error;
    }
};

const fetchItems = async (projectId) => { 
    try {
        const response = await axios.get(API_URL + 'items/?project=' + projectId);
        return response.data;
    } catch (error) {
        console.error('Error fetching items:', error);
        throw error;
    }
}

export { register, login, fetchProjects };