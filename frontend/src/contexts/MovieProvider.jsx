import React, { useState, useEffect, useCallback } from "react";
import { MovieContext } from "./MovieContext";
import {
  addFavoriteToAPI,
  getFavoriteAPI,
  removeFavoriteAPI,
} from "../services/api.js";

export const MovieProvider = ({ children }) => {
  const [favorites, setFavorites] = useState(() => {
    const storedFavs = localStorage.getItem("favorites");
    return storedFavs ? JSON.parse(storedFavs) : [];
  });
  const loadFavorites = async () => {
    try {
      const favoriteMovies = await getFavoriteAPI();
      setFavorites(favoriteMovies);
    } catch (error) {
      console.warn("Failed to load API", error.message);
    }
  };

  const reloadFavorites = useCallback(async () => {
    await loadFavorites();
  }, []); // no dependencies, so stable function

  useEffect(() => {
    reloadFavorites();
  }, [reloadFavorites]);

  useEffect(() => {
    const fetchFavorites = async () => {
      await loadFavorites();
    };
    fetchFavorites();
  }, []);

  const addToFavorites = async (movie) => {
    try {
      // Add to react state immediately for instant UI feedback
      setFavorites((prev) => [...prev, movie]);
      // Try to add to API
      await addFavoriteToAPI(movie);
      console.log(`Added Movie ID ${movie.id} from Favorite`);
    } catch (error) {
      console.error("Failed to add to API:", error.message);
      // Don't remove from local state - keep the optimistic update
    }
  };
  const removeFromFavorites = async (movieId) => {
    // Remove favorite from database
    await removeFavoriteAPI(movieId);

    reloadFavorites();
  };

  const isFavorite = (movieId) => {
    return favorites.some(
      (movie) => movie.id === movieId || movie.movie_id === movieId
    );
  };

  const value = {
    favorites,
    addToFavorites,
    removeFromFavorites,
    isFavorite,
    reloadFavorites,
  };

  return (
    <MovieContext.Provider value={value}>{children}</MovieContext.Provider>
  );
};
