//import logo from './logo.svg';
import './App.css';
import BookPage from './BookPage';
import SearchPage from './SearchPage';
//import HomePage from './HomePage';
import {
  BrowserRouter as Router, Routes, Route
} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/book" element={<BookPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
