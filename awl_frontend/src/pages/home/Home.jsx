import "./home.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import {views} from "react-big-calendar/lib/utils/constants";
import Sidebar from "../../components/sidebar/Sidebar";
import CalendarEvent from "../../components/calendar-event/CalendarEvent";
import React, {useEffect} from "react";
import {getSchedule} from "../../services/schedule/ScheduleService";
import {FormProvider, useForm} from "react-hook-form"

const localizer = momentLocalizer(moment)

const messages={
      previous: 'poprzedni',
      next: 'następny',
      today: 'dziś',
}
export default function Home() {
    const filterForm = useForm(
        {defaultValues: {groups: null, lecturers: null, rooms: null}}
    )
    const [schedule, setSchedule] = React.useState([]);
    const [selectedWeek, setSelectedWeek] = React.useState(null);
    const [scheduleQuery, setScheduleQuery] = React.useState({});

    function getWeekFromDate(date) {
        const startOfWeek = new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate() - date.getDay() + 1
        )
        const endOfWeek = new Date(
            date.getFullYear(), date.getMonth(), startOfWeek.getDate() + 6
        )
        return {
            date_from: moment(startOfWeek).format("YYYY-MM-DD"),
            date_to: moment(endOfWeek).format("YYYY-MM-DD")
        }
    }
    function onWeekChange(selected_date) {
        setSelectedWeek(getWeekFromDate(selected_date))
    }
    const getFullSchedule = async () => {
        if ("groups" in scheduleQuery || "rooms" in scheduleQuery || "lecturers" in scheduleQuery) {
            const response = await getSchedule(scheduleQuery);
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
    }
    function handleFormSubmit(data) {
        let week_query = selectedWeek
        if (selectedWeek === null) week_query = getWeekFromDate(new Date())
        setScheduleQuery({...scheduleQuery, ...data, ...week_query})
    }

    useEffect(() => {
        setScheduleQuery({...scheduleQuery, ...selectedWeek})
    },[selectedWeek])

    useEffect(() => {
        getFullSchedule();
    },[scheduleQuery])

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
                  onNavigate={onWeekChange}
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
