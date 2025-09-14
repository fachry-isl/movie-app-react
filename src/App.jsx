import "./css/App.css";
import MovieCard from "./components/MovieCard";
import Home from "./pages/Home";
import Favorites from "./pages/Favorites";
import { Routes, Route } from "react-router-dom";
import NavBar from "./pages/Navbar";
import { MovieProvider } from "./contexts/MovieContext";
import MovieDetail from "./pages/MovieDetail";

function App() {
  return (
    <MovieProvider>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/movie/:id" element={<MovieDetail />} />
      </Routes>
    </MovieProvider>
  );
}

export default App;
