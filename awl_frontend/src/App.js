import './App.css';
import Topbar from "./components/topbar/Topbar";
import Home from "./pages/home/Home";
import Footer from "./components/footer/Footer";
import Schedule from "./pages/schedule/Schedule";
import {BrowserRouter, Route, Routes} from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
        <div className="App">
            <Topbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/schedule" element={<Schedule />} />
                </Routes>
            <Footer />
        </div>
    </BrowserRouter>
  );
}

export default App;
