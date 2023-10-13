import "./home.css";
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import React from "react";
import {FormProvider, useForm} from "react-hook-form"
import {getAllGroups} from "../../services/groups/GroupService";
import { useNavigate } from 'react-router-dom';

export default function Home() {
    const navigate = useNavigate();
    const groupForm = useForm({defaultValues: {group: null}})
    const [groups, setGroups] = React.useState([]);

    React.useEffect(() => {
        const getGroups = async () => {
            const response = await getAllGroups();
            setGroups(
                response.map(group => ({...group, id: group.id.toString()}))
            );
        }
        getGroups();
    }, []);

    function handleFormSubmit(data) {
        if (data.group) {
            navigate(`/schedule?groups=${data.group}`);
        }
        else {
            navigate("/schedule");
        }
    }

    return (
        <div className="home-container">
            <FormProvider {...groupForm}>
                <form className="group-form" onSubmit={groupForm.handleSubmit(handleFormSubmit)}>
                    <h1 className="group-form-label">Wybierz grupę aby wyświetlić plan</h1>
                    <select {...groupForm.register("group")} className="group-form-select">
                        <option selected hidden disabled key={`form-option-default`} value={null}></option>
                        {groups.map((group) =>
                            <option key={`form-option_${group.id}`} value={group.id}>{group.name}</option>
                        )}
                    </select>
                    <button className="group-form-submit-button" type="submit">WYSZUKAJ</button>
                </form>
            </FormProvider>
        </div>
    );
}
