import {api} from '../boot/axios';
import axios from 'axios';
let url = process.env.API_URL
let conf = {baseURL: url, withCredentials: true}
export function home() {
    return api.get("/home")
}

export function features() {
    return api.get("/features")
}

export function login(username, password) {
    return api.post("/login", {username: username, password: password});
}

export function signup(username, password, email, firstName, lastName, membership) {
    
    return api.post("/signup",{ 
        username: username,
        password: password,
        first_name: firstName,
        email_address: email,
        last_name: lastName,
        membership: membership
    })
}

export function logout() {
    return axios.get( "/logout", conf)
}
export function createDatabase(username) {
    return axios.post(`/users/${username}/databases`, conf)
}
export function viewDatabase(username) {
    return axios.get(`/users/${username}/databases`, conf)
}
export function daleteDatabases(username) {
    return axios.delete(`/users/${username}/databases`, conf)
}
export function viewRecords(username, database_title) {
    return axios.get(`/users/${username}/databases/${database_title}`, conf)
}
export function renameDatabase(username, database_title) {
    return axios.put(`/users/${username}/databases/${database_title}`, conf)
}
export function deleteDatabase(username, database_title) {
    return axios.delete(`/users/${username}/databases/${database_title}`, conf)
}
export function addRecord(username, database_title) {
    return axios.post(`/users/${username}/databases/${database_title}`, conf)
}
export function viewRecord(username, database_title, pk) {
    return axios.get(`/users/${username}/databases/${database_title}/${pk}`, conf)
}
export function removeRecord(username, database_title, pk) {
    return axios.delete(`/users/${username}/databases/${database_title}/${pk}`, conf)
}
export function viewProfile(username) {
    return axios.get(`/users/${username}/profile`, conf)
}
export function viewFeatures() {
    return api.get("/features")
}
