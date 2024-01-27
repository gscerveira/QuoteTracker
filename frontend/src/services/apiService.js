import axios from 'axios';

axios.default.xsrfCookieName = 'csrftoken';
axios.default.xsrfHeaderName = 'X-CSRFToken';

const API_URL = 'http://localhost:8000/tracker_app/';

const register = (username, email, password) => {
    return axios.post(API_URL + 'register/', {
        username,
        email,
        password
    });
};

const login = (username, password, csrfToken) => {
    return axios.post(API_URL + 'login/', {
        username,
        password
    }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        withCredentials: true
    });
};

const fetchProjects = async () => {
    try {
        const response = await axios.get(API_URL + 'projects/', { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching projects:', error);
        throw error;
    }
};

const createProject = async (projectData) => {
    try {
        const response = await axios.post(API_URL + 'projects/', projectData, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error creating project:', error);
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
        const response = await axios.post(API_URL + 'items/', itemData, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error creating item:', error);
        throw error;
    }
};

const fetchQuoteRequests = async (itemId) => {
    try {
        const response = await axios.get(API_URL + 'quoterequests/?item=', itemId, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching quote requests:', error);
        throw error;
    }
};

const createQuoteRequest = async (quoteRequestData) => {
    try {
        const response = await axios.post(API_URL + 'quoterequests/', quoteRequestData, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error creating quote request:', error);
        throw error;
    }
};

const fetchStores = async () => {
    try {
        const response = await axios.get(API_URL + 'stores/', { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error fetching stores:', error);
        throw error;
    }
};

const createStore = async (storeData) => {
    try {
        const response = await axios.post(API_URL + 'stores/', storeData, { withCredentials: true });
        return response.data;
    } catch (error) {
        console.error('Error creating store:', error);
        throw error;
    }
};

export { register, login, fetchProjects, createProject, fetchItems, createItem, fetchQuoteRequests, createQuoteRequest, fetchStores, createStore };