import React from "react";
import "../css/MovieCard.css";
import { useMovieContext } from "../contexts/MovieContext";
import { useNavigate } from "react-router-dom";

const MovieCard = ({ movie }) => {
  const { isFavorite, addToFavorites, removeFromFavorites } = useMovieContext();
  const movieId = movie.id ?? movie.movie_id;
  const favorite = isFavorite(movieId);

  function onFavoriteClick(e) {
    e.preventDefault();
    if (favorite) removeFromFavorites(movieId);
    else addToFavorites(movie);
  }

  // Exercise: Add Navigation to Detail Page
  const navigate = useNavigate();
  function handleDetailClick() {
    navigate(`/movie/${movieId}`, { state: { movie } });
  }

  return (
    <div className="movie-card">
      <div className="movie-poster">
        <img
          src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
          alt={movie.title}
        />
        <div className="movie-overlay">
          <button
            className={`favorite-btn ${favorite ? "active" : ""}`}
            onClick={onFavoriteClick}
          >
            ♥
          </button>
        </div>
      </div>
      <div className="movie-info">
        <h3>{movie.title}</h3>
        <p>{movie.release_date?.split("-")[0]}</p>
      </div>

      <button className="detail-btn" type="button" onClick={handleDetailClick}>
        Detail
      </button>
    </div>
  );
};

export default MovieCard;
