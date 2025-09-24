import { Link } from "react-router-dom";
import "../css/Navbar.css";

import { useAuth } from "../contexts/useAuth";

function NavBar() {
  const { logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Movie App</Link>
      </div>
      <div className="navbar-links">
        <Link to="/" className="nav-link">
          Home
        </Link>
        <Link to="/favorites" className="nav-link">
          Favorites
        </Link>
        <button className="nav-link logout" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default NavBar;
