let URL = "http://127.0.0.1:5000"

export const get_home = await fetch(URL + "/", { method: "GET" }).then(resp => { return resp.json() })

export const features = await fetch(URL + "/features", { method: "GET" }).then(resp => { return resp.json() })

export async function login(username, password) {
    let formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    await fetch(URL + "/login", { method: "POST", body: formData })
        .then(resp => { console.log("axios resp", resp); return resp; })
}

export function signup(username, password, email, firstName, lastName, membership) {
    let formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("first_name", firstName);
    formData.append("email_address", email);
    formData.append("last_name", lastName);
    formData.append("membership", membership);
    fetch(URL + "/signup", {
        method: "post",
        body: formData,
    })
        .then(resp => { console.log(resp); return resp.json(); })
}
