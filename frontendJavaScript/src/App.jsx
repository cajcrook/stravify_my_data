import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import Dashboard from './pages/Dashboard/Dashboard.jsx';


function App() {
    return (
        <div className="App">
            <Dashboard />

        </div>
    );
}

export default App;