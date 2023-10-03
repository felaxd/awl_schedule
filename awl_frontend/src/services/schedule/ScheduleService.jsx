import {config} from "../config";

export async function getSchedule(data) {
    let queryParams = ""
    console.log(data)
    if (data.groups) {
        queryParams += "&groups=" + data.groups.join("&groups=") + "&"
    }
    if (data.lecturers) {
        queryParams += "&lecturers=" + data.lecturers.join("&lecturers=") + "&"
    }
    if (data.rooms) {
        queryParams += "&rooms=" + data.rooms.join("&rooms=") + "&"
    }
    queryParams = queryParams.replace(/&$/, '');
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
