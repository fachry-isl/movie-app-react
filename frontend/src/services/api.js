const API_KEY = "27490be72a2cbd88c2a5c2fd9fd45af7";
const BASE_URL = "https://api.themoviedb.org/3";

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
