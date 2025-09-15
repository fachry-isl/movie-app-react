import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../css/MovieDetail.css";

const genreMap = {
  28: "Action",
  12: "Adventure",
  16: "Animation",
  35: "Comedy",
  80: "Crime",
  99: "Documentary",
  18: "Drama",
  10751: "Family",
  14: "Fantasy",
  36: "History",
  27: "Horror",
  10402: "Music",
  9648: "Mystery",
  10749: "Romance",
  878: "Science Fiction",
  10770: "TV Movie",
  53: "Thriller",
  10752: "War",
  37: "Western",
};

const MovieDetail = () => {
  const { state } = useLocation();
  const navigate = useNavigate();
  const movie = state?.movie;

  if (!movie) {
    return <div>No movie data found.</div>;
  }

  const genres = movie.genres
    ? movie.genres.map((g) => g.name).join(", ")
    : movie.genre_ids
    ? movie.genre_ids.map((id) => genreMap[id] || id).join(", ")
    : "Unknown";

  return (
    <div className="movie-detail-container">
      <div className="movie-detail-image-wrapper">
        <img
          src={`https://image.tmdb.org/t/p/w780${
            movie.backdrop_path || movie.poster_path
          }`}
          alt={movie.title}
          className="movie-detail-image"
        />
        <button
          onClick={() => navigate(-1)}
          className="movie-detail-back-btn"
          title="Back"
        >
          ↩️
        </button>
      </div>
      <div className="movie-detail-content">
        <h1 className="movie-detail-title">{movie.title}</h1>
        <div className="movie-detail-meta">
          {movie.release_date?.split("-")[0]} &bull; {genres}
        </div>
        <div className="movie-detail-rating-row">
          <span className="movie-detail-rating">
            ★ {movie.vote_average?.toFixed(1) || "N/A"}
          </span>
          <span className="movie-detail-votes">{movie.vote_count} votes</span>
        </div>
        <p className="movie-detail-overview">
          {movie.overview || "No description available."}
        </p>
        <div className="movie-detail-stats">
          <div>
            <strong>Original Language:</strong>{" "}
            {movie.original_language?.toUpperCase()}
          </div>
          <div>
            <strong>Popularity:</strong> {movie.popularity}
          </div>
          <div>
            <strong>Release Date:</strong> {movie.release_date}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;
