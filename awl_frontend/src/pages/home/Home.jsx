import "./home.css";
import { Calendar, momentLocalizer } from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/pl';
import "react-big-calendar/lib/css/react-big-calendar.css";
import {views} from "react-big-calendar/lib/utils/constants";
import Sidebar from "../../components/sidebar/Sidebar";

const localizer = momentLocalizer(moment)

const messages={
      previous: 'poprzedni',
      next: 'następny',
      today: 'dziś',
}

export default function Home() {
  return (
      <>
          <Sidebar />
          <div className="calendar">
              <Calendar
                  localizer={localizer}
                  events={[]}
                  showAllEvents={true}
                  min={new Date(0, 0, 0, 8, 0, 0)}
                  max={new Date(0, 0, 0, 22, 0, 0)}
                  views={[views.WEEK]}
                  defaultView={views.WEEK}
                  style={{ height: 700 }}
                  messages={messages}
              />
          </div>
      </>

  );
}
