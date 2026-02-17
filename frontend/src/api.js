import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000',
});

// Token hozzáadása minden kéréshez, ha be vagyunk jelentkezve
api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(response => response, error => {
    if (error.response && error.response.status === 401) {
        // Ha lejár a token vagy érvénytelen, kijelentkeztethetjük a felhasználót (opcionális)
        // localStorage.removeItem('access_token');
        // window.location.href = '/login';
    }
    return Promise.reject(error);
});

export default api;