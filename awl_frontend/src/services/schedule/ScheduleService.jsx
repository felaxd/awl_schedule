import {config} from "../config";

function getQueryParams(data) {
    let queryParams = ""
    if (data.groups?.length > 0) {
        queryParams += "groups=" + data.groups.join("&groups=") + "&"
    }
    if (data.lecturers?.length > 0) {
        queryParams += "lecturers=" + data.lecturers.join("&lecturers=") + "&"
    }
    if (data.rooms?.length > 0) {
        queryParams += "rooms=" + data.rooms.join("&rooms=") + "&"
    }
    if (data.date_from) {
        queryParams += "date_from=" + data.date_from + "&"
    }
    if (data.date_to) {
        queryParams += "date_to=" + data.date_to + "&"
    }
    queryParams = queryParams.replace(/&$/, '');
    return queryParams
}

export async function getSchedule(data) {
    const queryParams = getQueryParams(data);
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
