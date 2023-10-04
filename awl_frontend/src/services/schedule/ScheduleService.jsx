import {config} from "../config";

export async function getSchedule(data) {
    let queryParams = ""
    console.log(data)
    if (data.groups?.length > 0) {
        queryParams += "groups=" + data.groups.join("&groups=") + "&"
    }
    if (data.lecturers?.length > 0) {
        queryParams += "lecturers=" + data.lecturers.join("&lecturers=") + "&"
    }
    if (data.rooms?.length > 0) {
        queryParams += "rooms=" + data.rooms.join("&rooms=") + "&"
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
