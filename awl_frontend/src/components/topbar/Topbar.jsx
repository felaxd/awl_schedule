import React from "react";
import "./topbar.css";
import {Link} from "react-router-dom";

export default function Topbar() {
    return (
        <div className="topbar">
            <Link to="/"><img className="logo" src="/logo.png" alt="AWL" /></Link>
        </div>
    );
}
