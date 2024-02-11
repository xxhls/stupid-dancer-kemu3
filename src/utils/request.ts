import axios from "axios";

const service = axios.create({
    baseURL: "http://127.0.0.1:8000/",
    timeout: 5000
});

service.interceptors.response.use((response) => {
    return Promise.resolve(response.data)
}, error => {
    return Promise.reject(error)
});

export default service;
