import "./home.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import {views} from "react-big-calendar/lib/utils/constants";
import Sidebar from "../../components/sidebar/Sidebar";
import CalendarEvent from "../../components/calendar-event/CalendarEvent";
import React from "react";

const localizer = momentLocalizer(moment)

const messages={
      previous: 'poprzedni',
      next: 'następny',
      today: 'dziś',
}
export const ScheduleContext = React.createContext(null);
export default function Home() {
    const [schedule, setSchedule] = React.useState([]);

  return (
      <ScheduleContext.Provider value={{schedule: schedule, setSchedule: setSchedule}}>
          <Sidebar />
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
      </ScheduleContext.Provider>

  );
}
