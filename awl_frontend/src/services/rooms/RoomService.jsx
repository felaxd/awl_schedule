import {config} from "../config";

export async function getAllRooms() {
    return fetch(`${config.API_URL}/rooms/`)
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
