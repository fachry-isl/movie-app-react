import "./css/App.css";

import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Favorites from "./pages/Favorites";
import Login from "./pages/Login";
import NavBar from "./pages/Navbar";
import MovieDetail from "./pages/MovieDetail";

import { MovieProvider } from "./contexts/MovieProvider";
import { AuthProvider } from "./contexts/AuthProvider";
import ProtectedRoute from "./pages/ProtectedRoute";

import { useLocation } from "react-router-dom";

function App() {
  // Use location to detect whether to show navigation
  const location = useLocation();

  const isShowNavigation = location.pathname !== "/login";

  return (
    <AuthProvider>
      <MovieProvider>
        {isShowNavigation && <NavBar />}
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route
            path="/favorites"
            element={
              <ProtectedRoute>
                <Favorites />
              </ProtectedRoute>
            }
          />
          <Route
            path="/movie/:id"
            element={
              <ProtectedRoute>
                <MovieDetail />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<Login />} />
        </Routes>
      </MovieProvider>
    </AuthProvider>
  );
}

export default App;
