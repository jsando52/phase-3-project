import { React, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./page-styles/bookPage.css"
function BookPage()
{
    const location = useLocation();
    const title   = location.state;
    const [message, setMessage] = useState("");
    const [bookData, setBookData] = useState([]);

    useEffect(() => async () =>
    {
        setMessage(title);
        console.log("Sending title to backend:", title);
        try
        {
            const response = await fetch("http://127.0.0.1:5000/book",
            {
                method: "POST",
                headers:
                {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(
                {
                    title: title,
                }),
            });
            const data = await response.json();
            setBookData(JSON.parse(data["book"]));
        }
        catch(err)
        {
            console.error(err);
        }
        
    }, [title]);


    const renderStats = (statsArray) => {
        if (!statsArray || statsArray.length === 0) return <p>No data available.</p>;
   
        const keys = Object.keys(statsArray[0]);
   
        return (
            <table className="table">
                <thead>
                    <tr>
                        {keys.map((key, index) => (
                            <th key={index}>{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {statsArray.map((statObj, rowIndex) => (
                        <tr key={rowIndex}>
                            {keys.map((key, colIndex) => (
                                <td key={colIndex}>{statObj[key]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };
   
    return (
        <div>
        <div className="table-div">
            <h2>{message} information</h2>
            {renderStats(bookData)}
        </div>

    </div>
    );
}
export default BookPage;
