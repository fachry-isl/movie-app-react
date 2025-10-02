// Movie API
const API_KEY = "27490be72a2cbd88c2a5c2fd9fd45af7";
const BASE_URL = "https://api.themoviedb.org/3";

// BACKEND URL
const BACKEND_URL = "http://127.0.0.1:8000";

// TMDB API Request
export const getPopularMovies = async () => {
  const response = await fetch(`${BASE_URL}/movie/popular?api_key=${API_KEY}`);
  const data = await response.json();
  return data.results;
};

export const searchMovies = async (query) => {
  const response = await fetch(
    `${BASE_URL}/search/movie?api_key=${API_KEY}&query=${encodeURIComponent(
      query
    )}`
  );
  const data = await response.json();
  return data.results;
};

// Backend API
// Simulated API login function
export const fakeApiLogin = (username, password) =>
  new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === "user" && password === "password") {
        resolve("fake-jwt-token-123456");
        console.log("Success Login");
      } else {
        reject("Invalid credentials");
      }
    }, 1000);
  });

export const userAuth = (username, password) =>
  new Promise((resolve, reject) => {
    // Add a small delay before making the request (like fakeApiLogin)
    setTimeout(() => {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      fetch(`${BACKEND_URL}/auth/jwt/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            reject(`HTTP error! status: ${response.status}`);
            return;
          }
          return response.json();
        })
        .then((data) => {
          if (data.access_token || data.token) {
            const token = data.access_token || data.token;
            console.log("Token received!");

            if (data.refresh_token) {
              localStorage.setItem("refresh_token", data.refresh_token);
            }

            console.log("Success Login");
            resolve(token);
          } else {
            reject("No token received from server");
          }
        })
        .catch((error) => {
          console.error("Login failed:", error.message || error);
          reject(error.message || error);
        });
    }, 1000); // 1 second delay before making request
  });

// // Check if token is expired
// const isTokenExpired = (token) => {
//   if (!token) return true;

//   try {
//     const payload = JSON.parse(atob(token.split(".")[1]));
//     return payload.exp * 1000 < Date.now();
//   } catch (error) {
//     console.log(error);
//     return true;
//   }
// };

// Get JWT token from localStorage
const getAuthToken = () => {
  return localStorage.getItem("authToken");
};
// TODO: Add Favorite Movie Endpoint
export const addFavoriteToAPI = async (movie) => {
  const token = getAuthToken();
  console.log(token);

  // if (!token || isTokenExpired(token)) {
  //   throw new Error("Token expired or missing");
  // }

  if (!token) {
    throw new Error("Token expired or missing");
  }

  const response = await fetch(`${BACKEND_URL}/favorites/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      movie_id: movie.id,
      title: movie.title || movie.name,
      overview: movie.overview || "No description available",

      release_date: movie.release_date,
      poster_path: movie.poster_path,
      vote_average: movie.vote_average,
      vote_count: movie.vote_count,
      genres: movie.genre_ids,
      popularity: movie.popularity,
      original_language: movie.original_language,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Unauthorized");
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
};

// TODO: Get Favorite API Implementation
export const getFavoriteAPI = async () => {
  const token = getAuthToken();
  console.log(token);

  const response = await fetch(`${BACKEND_URL}/favorites/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Unauthorized");
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  // Map movie_name to title for each entry
  const data_test = data.map((favorite) => ({
    ...favorite.movie,
  }));

  console.log(data_test);

  return data_test;
};

// TODO: Remove Favorite API Implementation
