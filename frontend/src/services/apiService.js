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

const fetchProjects = () => {
    return axios.get(API_URL + 'projects-list/');
};

export { register, login, fetchProjects };