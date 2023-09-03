import "./home.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment)

export default function Home() {
  return (
    <div className="home">
    <Calendar
      localizer={localizer}
      events={[]}
      defaultDate={new Date()}
      startAccessor="start"
      endAccessor="end"
      resourceIdAccessor="id"
      style={{ height: 500 }}
    />
    </div>
  );
}
