import React from "react";
import { useNavigate } from "react-router-dom";
import "./page-styles/Header.css"; // Import the CSS file

function Header() {
    const navigator = useNavigate(); // navigates to other pages

    function homeFunction() {
        navigator("/");
    }

    function searchFunction() {
        navigator("/search");
    }

    return (
        <div className="container">
                <button className="homeButton" onClick={homeFunction}>Home</button>
                <button className="Button" onClick={searchFunction}>Search</button>
        </div>
    );
}

export default Header;