import {api} from '../boot/axios';

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
    return api.get( "/logout")
}
export function createDatabase(username) {
    return api.post(`/users/${username}/databases`)
}
export function viewDatabase(username) {
    return api.get(`/users/${username}/databases`)
}
export function daleteDatabases(username) {
    return api.delete(`/users/${username}/databases`)
}
export function viewRecords(username) {
    return api.get(`/users/${username}/databases`)
}
export function renameDatabase(username, database_title) {
    return api.put(`/users/${username}/databases/${database_title}`)
}
export function deleteDatabase(username, database_title) {
    return api.delete(`/users/${username}/databases/${database_title}`)
}
export function addRecord(username, database_title) {
    return api.post(`/users/{username}/databases/{database_title}`)
}
export function viewRecord(username, database_title, pk) {
    return api.get(`/users/${username}/databases/${database_title}/${pk}`)
}
export function removeRecord(username, database_title, pk) {
    return api.delete(`/users/${username}/databases/${database_title}/${pk}`)
}
export function viewProfile(username) {
    return api.get(`/users/${username}/profile`)
}
export function viewFeatures() {
    return api.get("/features")
}
