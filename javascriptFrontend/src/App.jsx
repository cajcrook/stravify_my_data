import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import "./App.css";
import StravaActivities from "./pages/StravaActivities/StravaActivities";

// import { HomePage } from "./pages/Home/HomePage";
// import { LoginPage } from "./pages/Login/LoginPage";
// import { SignupPage } from "./pages/Signup/SignupPage";
// import { UserPage } from "./pages/User/UserPage";
// import 'bootstrap/dist/css/bootstrap.min.css';

// Component to handle conditional rendering of the Header
// const Layout = ({ children }) => {
  // const location = useLocation();
  // Hide the header for the /login, /signup, and / paths
//   const hideHeaderPaths = ["/login", "/signup", "/"];
//   const shouldHideHeader = hideHeaderPaths.includes(location.pathname);
//   return (
//     <>
//       <div className="main-content">
//         {!shouldHideHeader && <Header />} {/* Show header unless it's a restricted path */}
//         {children}
//       </div>
//     </>
//   );
// };

function App() {
    return (
        <div className="App">
            <StravaActivities />
        </div>
    );
}

export default App;