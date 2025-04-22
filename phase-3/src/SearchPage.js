import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./page-styles/SearchPage.css"; // Import the external CSS file

function SearchPage() {
  const navigator = useNavigate();
  const [filter, setFilter] = useState("Sort By Title");
  const [sort, setSort] = useState("ASC");
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState("");

  const options = ["Sort By Title", "Sort By Retailer", "Sort By Price"];
  const sorting = ["ASC", "DESC"];

  function playerFunction(row) {
    navigator("/player", { state:  row.Name });
  }

  const sendMessage = async () => 
  {
    if (query.trim() === "") 
    {
      return;
    }
    try
    {
      const response = await fetch("http://127.0.0.1:5000/search", 
      {
          method: "POST",
          headers: 
          {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(
            {
              Filter: filter,
              Sort: sort,
              Query: query,
            }),
      });
      const data = await response.json();
      setResults(JSON.parse(data));
      setQuery("");
    }
    catch (err)
    {
      console.error(err);
    }
  }

  return (
    <div>
      
        <div>
          <div className="filterContainer">
            <p>Filter</p>
            <select onChange={(e) => setFilter(e.target.value)} className="filter">
              {options.map((option, index) => (
                <option key={index}>{option}</option>
              ))}
            </select>
            <select onChange={(e) => setSort(e.target.value)} className="filter">
              {sorting.map((option, index) => (
                <option key={index}>{option}</option>
              ))}
            </select>
          </div>

          <div className="searchContainer">
            <input
              className="inputWrapper"
              placeholder="Type to search..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button className="searchButton" onClick={sendMessage}>
              <span className="searchText">Search</span>
            </button>
          </div>

          {/* Display search results */}
          <div className="resultsContainer">
            {results.length === 0 ? (
              <p>No results found. Try a different search.</p>
            ) : (
              <ul>
                {results.map((input, index) => (
                  <li key={index}>
                    <pre>
                      <button onClick={() => playerFunction(input)}>
                        {JSON.stringify(input, (key, value) =>
                          key === "Valid" ? undefined : value
                        )
                          .slice(2, -2)
                          .replaceAll("\"", "")
                          .replaceAll(",", "\n")
                          .replaceAll(":", ": ")
                          .replaceAll(";", ":")}
                      </button>
                    </pre>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
    </div>
  );
}

export default SearchPage;