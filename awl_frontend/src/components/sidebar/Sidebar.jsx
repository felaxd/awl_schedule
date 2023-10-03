import React from "react";
import "./sidebar.css";
import SidebarFilter from "../sidebar-filter/SidebarFilter";
import {getAllGroups} from "../../services/groups/GroupService";
import {getAllLecturers} from "../../services/lecturers/LecturerService";
import {getAllRooms} from "../../services/rooms/RoomService";

export default function Sidebar() {
    const [groups, setGroups] = React.useState([]);
    const [lecturers, setLecturers] = React.useState([]);
    const [rooms, setRooms] = React.useState([]);

    React.useEffect(() => {
        const getGroups = async () => {
            const response = await getAllGroups();
            setGroups(
                response.map(group => ({...group, id: group.id.toString()}))
            );
        }
        const getLecturers = async () => {
            const response = await getAllLecturers();
            setLecturers(
                response.map(lecturer => ({...lecturer, name: `${lecturer.last_name} ${lecturer.first_name}`}))
            );
        }
        const getRooms = async () => {
            const response = await getAllRooms();
            setRooms(response);
        }
        getGroups();
        getLecturers();
        getRooms();
    }, []);
    return (
        <div className="sidebar">
            <span className="sidebar-description">Filtrowanie</span>
            <div className="sidebar-filters">
                {groups && <SidebarFilter filter_title="Grupy" form_key="groups" options={groups}/>}
                {lecturers && <SidebarFilter filter_title="Prowadzący" form_key="lecturers" options={lecturers}/>}
                {rooms && <SidebarFilter filter_title="Sale" form_key="rooms" options={rooms}/>}
            </div>
            <button type="submit">Zatwierdź</button>
        </div>
    );
}
