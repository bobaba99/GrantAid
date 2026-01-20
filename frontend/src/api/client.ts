import axios from 'axios';
import { getSession } from './auth';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(async (config) => {
    const { data } = await getSession();
    if (data?.session?.access_token) {
        config.headers.Authorization = `Bearer ${data.session.access_token}`;
    }
    return config;
});
