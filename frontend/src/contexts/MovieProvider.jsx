import React, { useState, useEffect, useCallback } from "react";
import { MovieContext } from "./MovieContext";
import { addFavoriteToAPI, getFavoriteAPI } from "../services/api.js";

export const MovieProvider = ({ children }) => {
  const [favorites, setFavorites] = useState(() => {
    const storedFavs = localStorage.getItem("favorites");
    return storedFavs ? JSON.parse(storedFavs) : [];
  });

  // TODO: Get Favorites from DB
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

  // TODO: Add Favorite Local and API Sync

  // OLD Implementation
  // const addToFavorites = (movie) => {
  //   setFavorites((prev) => [...prev, movie]);
  // };

  const addToFavorites = async (movie) => {
    try {
      // Add to local state immediately for instant UI feedback
      setFavorites((prev) => [...prev, movie]);
      console.log("Added to local favorites:", movie);

      // Try to add to API
      await addFavoriteToAPI(movie);
      console.log("Successfully added to API:", movie);
    } catch (error) {
      console.error("Failed to add to API:", error.message);
      // Don't remove from local state - keep the optimistic update
    }
  };

  // TODO: Remove Favorite Local and API Sync
  // const removeFromFavorites = (movieId) => {
  //   setFavorites((prev) => prev.filter((movie) => movie.id != movieId));
  // };

  const removeFromFavorites = async (movieId) => {
    // Remove favorite from local storage
    setFavorites((prev) => prev.filter((movie) => movie.id != movieId));

    // Remove favorite from database
  };

  const isFavorite = (movieId) => {
    return favorites.some((movie) => movie.id === movieId);
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
