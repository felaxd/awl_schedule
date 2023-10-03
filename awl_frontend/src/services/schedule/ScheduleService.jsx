import {config} from "../config";

export async function getSchedule(data) {
    const queryParams = new URLSearchParams(data);
    return fetch(`${config.API_URL}/schedule/?${queryParams}`)
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
