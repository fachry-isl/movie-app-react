// Movie API
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

export const userAuth = (username, password) =>
  new Promise((resolve, reject) => {
    // Add a small delay before making the request (like fakeApiLogin)
    setTimeout(() => {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      fetch("http://127.0.0.1:8000/auth/jwt/login/", {
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
