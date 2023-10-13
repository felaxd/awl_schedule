import "./calendareventmodal.css";
import React from "react";
import {Box, Modal, Typography} from "@mui/material";
import moment from "moment/moment";

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};
export default function CalendarEventModal({modalState, setModalState, event}) {
    const lecturer_rooms = event.lecturers.map((lecturer_obj) => {
        return lecturer_obj.room?.id
    })
    const rooms_with_no_lecturer = event.rooms.filter(room => {
        return !lecturer_rooms.includes(room.id);
    });
    const handleClose = () => setModalState(false);
    return (
        <Modal
            open={modalState}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
                <Typography variant="h6" component="h2">
                    {[moment(event.start).format("HH:MM"), moment(event.end).format("HH:MM")].join(" - ")}
                    <br/>
                    {event.course_name}
                </Typography>
                <Typography sx={{ mt: 1 }}>{event.type}</Typography>
                <Typography sx={{ mt: 2 }}>
                    Grupy:<br/>
                    {event.groups.map((group) => {
                        return (<>{group.name}<br/></>);
                    })}
                </Typography>
                <Typography sx={{ mt: 2 }}>
                    Prowadzący/Sala:<br/>
                    {event.lecturers.map((lecturer_obj) => {
                        const lecturer_name = [
                            lecturer_obj?.lecturer?.title,
                            lecturer_obj?.lecturer?.last_name,
                            lecturer_obj?.lecturer?.first_name
                        ].join(" ")
                        return (<>{lecturer_name} - {lecturer_obj.room?.name}<br/></>);
                    })}
                    {rooms_with_no_lecturer.map((room) => room.name)}
                </Typography>
            </Box>
        </Modal>
    );
}

