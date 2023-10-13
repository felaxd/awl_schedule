import React from "react";
import "./topbar.css";
import {Link} from "react-router-dom";
import {config} from "../../services/config";
import {Button} from "@mui/material";

export default function Topbar() {
    return (
        <div className="topbar">
            <Link to="/"><img className="logo" src="/logo.png" alt="AWL" /></Link>
            <Link className="topbar-login-container" to={config.ADMIN_SITE_URL}>
                <Button id="topbar-login-button">Zaloguj</Button>
            </Link>
        </div>
    );
}
