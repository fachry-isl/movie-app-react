import React, { createContext, useState } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem("authToken"));

  const login = (token) => {
    localStorage.setItem("authToken", token);
    setToken(token);
  };

  const logout = () => {
    localStorage.removeItem("authToken");
    setToken(null);
  };

  const value = {
    token,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
