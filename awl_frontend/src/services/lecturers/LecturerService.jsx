import {config} from "../config";

export async function getAllLecturers() {
    return fetch(`${config.API_URL}/lecturers/`)
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
