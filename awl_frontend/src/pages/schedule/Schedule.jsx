import "./schedule.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import {views} from "react-big-calendar/lib/utils/constants";
import Sidebar from "../../components/sidebar/Sidebar";
import CalendarEvent from "../../components/calendar-event/CalendarEvent";
import React, {useEffect} from "react";
import {getSchedule, getQueryParams} from "../../services/schedule/ScheduleService";
import {FormProvider, useForm} from "react-hook-form"
import {useLocation, useNavigate} from "react-router-dom";
import CalendarEventModal from "../../components/calendar-event-modal/CalendarEventModal";

const localizer = momentLocalizer(moment)

const messages={
      previous: 'poprzedni',
      next: 'następny',
      today: 'dziś',
}

function useQuery() {
    const { search } = useLocation();
    return React.useMemo(() => new URLSearchParams(search), [search]);
}

export default function Schedule() {
    const navigate = useNavigate();
    const urlParams = useQuery();
    const filterForm = useForm(
        {defaultValues: {groups: null, lecturers: null, rooms: null}}
    )
    const [schedule, setSchedule] = React.useState([]);
    const [selectedWeek, setSelectedWeek] = React.useState(null);
    const [scheduleQuery, setScheduleQuery] = React.useState({});

    const [selectedEvent, setSelectedEvent] = React.useState(null)
    const [modalState, setModalState] = React.useState(false)

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

    useEffect(() => {
        const selected_options = Array.from(urlParams.entries())
        if (selected_options.length) {
            let weekQuery = selectedWeek
            if (selectedWeek === null) weekQuery = getWeekFromDate(
                urlParams.get("date_from") ? new Date(urlParams.get("date_from")) : new Date()
            )
            let dataQuery = {
                groups: [], lecturers: [], rooms: []
            }
            let isQueryGood = false
            selected_options.map((option) => {
                if (option[0] === "groups" && option[1]) {
                    dataQuery.groups.push(option[1])
                    isQueryGood = true
                }
                if (option[0] === "lecturers" && option[1]) {
                    dataQuery.lecturers.push(option[1])
                    isQueryGood = true
                }
                if (option[0] === "rooms" && option[1]) {
                    dataQuery.rooms.push(option[1])
                    isQueryGood = true
                }
            })
            if (isQueryGood) {
                filterForm.setValue("groups", dataQuery.groups)
                filterForm.setValue("lecturers", dataQuery.lecturers)
                filterForm.setValue("rooms", dataQuery.rooms)
                const fullQuery = {...scheduleQuery, ...dataQuery, ...weekQuery}
                setScheduleQuery(fullQuery);
                setSelectedWeek(weekQuery);
                getFullSchedule(fullQuery);
            }
        }
    },[])

    const onWeekChange = (selected_date) => {
        const weekDate = getWeekFromDate(selected_date);
        setSelectedWeek(weekDate);
        const query = {...scheduleQuery, ...weekDate};
        setScheduleQuery(query)
        getFullSchedule(query);
        navigate("/schedule?" + getQueryParams(query))
    }

    const getFullSchedule = async (query) => {
        if (query.groups?.length || query.rooms?.length || query.lecturers?.length) {
            const response = await getSchedule(query);
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
        else setSchedule([])
    }
    function handleFormSubmit(data) {
        let weekQuery = selectedWeek
        if (selectedWeek === null) weekQuery = getWeekFromDate(new Date())
        const query = {...scheduleQuery, ...data, ...weekQuery}
        setScheduleQuery(query);
        getFullSchedule(query);
        navigate("/schedule?" + getQueryParams(query))
    }

    function handleSelectedEvent (event) {
        setSelectedEvent(event)
        setModalState(true)
    }

  return (
      <div className="schedule-container">
          {selectedEvent && <CalendarEventModal event={selectedEvent} modalState={modalState} setModalState={setModalState}/>}
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
                  date={selectedWeek?.date_from ?? new Date()}
                  onNavigate={onWeekChange}
                  onSelectEvent={handleSelectedEvent}
                  views={[views.WEEK]}
                  defaultView={views.WEEK}
                  style={{ height: 700 }}
                  messages={messages}
                  components={{
                      event: CalendarEvent
                  }}
              />
          </div>
    </div>
  );
}
