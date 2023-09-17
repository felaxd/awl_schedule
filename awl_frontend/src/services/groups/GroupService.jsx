import {config} from "../config";

export async function getAllGroups() {
    return fetch(`${config.API_URL}/groups/`)
        .then((response) => {
            return response.json()
        })
        .then((result) => {
            return result;
        })
        .catch((error) => {
            console.log(error)
            return [];
        });
}
