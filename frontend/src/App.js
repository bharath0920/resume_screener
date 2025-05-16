import React from "react";
import ResumeScreeningForm from "./components/ResumeScreeningForm";
import "./App.css";
import logo from "./assets/logo.jpg";

function App() {
  return (
    <div className="app-root">
      <div className="sidebar">
        <img src={logo} alt="Company Logo" className="logo" />
      </div>
      <div className="main-content">
        <ResumeScreeningForm />
      </div>
    </div>
  );
}

export default App;
