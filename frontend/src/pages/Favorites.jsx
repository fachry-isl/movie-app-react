import "../css/Favorites.css";
import { useMovieContext } from "../contexts/MovieContext";
import MovieCard from "../components/MovieCard";

import { useEffect } from "react";

function Favorite() {
  const { favorites, reloadFavorites } = useMovieContext();

  useEffect(() => {
    reloadFavorites();
  }, [reloadFavorites]);

  if (favorites.length === 0) {
    return (
      <div className="favorites-empty">
        <h2>No Favorite Movies Yet</h2>
        <b>Start adding movies to your favorites and they will appear here.</b>
      </div>
    );
  }

  return (
    <div className="movies-grid">
      {favorites.map((movie) => (
        <MovieCard movie={movie} key={movie.movie_id || movie.id} />
      ))}
    </div>
  );
}

export default Favorite;
