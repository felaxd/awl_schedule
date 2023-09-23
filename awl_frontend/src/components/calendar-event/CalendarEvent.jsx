import "./calendarevent.css";
import React from "react";

export default function CalendarEvent(props) {
    const lecturer_rooms = props.event.lecturers.map((lecturer_obj) => {
        return lecturer_obj.room?.id
    })
    const rooms_with_no_lecturer = props.event.rooms.filter(room => {
        return !lecturer_rooms.includes(room.id);
    });

    return <div className="rbc-custom-event">
        <div className="course-info-container">
            <div className="course-name">{props.event.course_name}</div>
            <div className="course-type">{props.event.type}</div>
        </div>
        <div className="group-container">
            {props.event.groups.map((group, i) =>
                <div key={i} className="group-name">{group.name}</div>
            )}
        </div>
        <div className="room-container">
            {props.event.lecturers.map((lecturer_obj, i) =>
                <div key={i} className="lecturer-room-container">
                    <div key={i} className="lecturer-name" title={`${lecturer_obj.lecturer.title} ${lecturer_obj.lecturer.last_name} ${lecturer_obj.lecturer.first_name}`}>
                        {lecturer_obj.lecturer.last_name} {lecturer_obj.lecturer.first_name}
                    </div>
                    <div key={i} className="lecturer-room">{lecturer_obj.room?.name}</div>
                </div>
            )}
            {rooms_with_no_lecturer.map((room, i) =>
                <div key={i} className="standalone-room-container">
                    <div key={i} className="room-name">{room.name}</div>
                </div>
            )}
        </div>
    </div>
}

