import Home from "./pages/home/Home";
import './App.css';
import Topbar from "./components/topbar/Topbar";

function App() {
  return (
    <div className="App">
        <Topbar />
        <div className="container">
            <Home />
        </div>
    </div>
  );
}

export default App;
