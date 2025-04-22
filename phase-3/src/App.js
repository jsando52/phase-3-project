//import logo from './logo.svg';
import './App.css';
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
        </Routes>
      </Router>
    </div>
  );
}

export default App;
