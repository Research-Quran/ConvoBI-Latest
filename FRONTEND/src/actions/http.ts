import axios from "axios";

const http = axios.create({
    baseURL: process.env.NEXT_PUBLIC_BASE_API_URL,
    headers: {
        "Content-Type": "application/json"
    }
})

export const setAuthToken = (token: string | null) => {
    if(token) {
        http.defaults.headers.common['Authorization'] = `Bearer ${token}`
        localStorage.setItem('kcToken', token)
    }else{
        delete http.defaults.headers.common['Authorization']
        localStorage.removeItem('kcToken')
    }
}

export default http