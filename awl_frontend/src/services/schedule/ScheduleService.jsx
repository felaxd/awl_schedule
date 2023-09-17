import {config} from "../config";

export async function getSchedule() {
    return fetch(`${config.API_URL}/schedule/`)
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
