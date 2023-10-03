import "./home.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import {views} from "react-big-calendar/lib/utils/constants";
import Sidebar from "../../components/sidebar/Sidebar";
import CalendarEvent from "../../components/calendar-event/CalendarEvent";
import React from "react";
import {getSchedule} from "../../services/schedule/ScheduleService";
import {FormProvider, useForm} from "react-hook-form"

const localizer = momentLocalizer(moment)

const messages={
      previous: 'poprzedni',
      next: 'następny',
      today: 'dziś',
}
export const ScheduleContext = React.createContext(null);
export default function Home() {
    const filterForm = useForm(
        {defaultValues: {groups: null, lecturers: null, rooms: null}}
    )
    const [schedule, setSchedule] = React.useState([]);

    function handleFormSubmit(data) {
        const getFullSchedule = async (data) => {
            const response = await getSchedule(data);
            setSchedule(response.map(block => (
                {
                    id: block.id,
                    title: `${block.course_name} - ${block.type}`,
                    start: new Date(block.start),
                    end: new Date(block.end),
                    lecturers: block.lecturers,
                    rooms: block.rooms,
                    groups: block.groups,
                    type: block.type,
                    course_name: block.course_name,
                }
            )));
        }
        getFullSchedule(data);
    }

  return (
      <>
          <FormProvider {...filterForm}>
              <form onSubmit={filterForm.handleSubmit(handleFormSubmit)}>
              <Sidebar />
              </form>
          </FormProvider>
          <div className="calendar">
              <Calendar
                  localizer={localizer}
                  dayLayoutAlgorithm = 'no-overlap'
                  events={schedule}
                  showAllEvents={true}
                  min={new Date(0, 0, 0, 8, 0, 0)}
                  max={new Date(0, 0, 0, 22, 0, 0)}
                  views={[views.WEEK]}
                  defaultView={views.WEEK}
                  style={{ height: 700 }}
                  messages={messages}
                  components={{
                      event: CalendarEvent
                  }}
              />
          </div>
    </>
  );
}
