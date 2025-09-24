// AuthContext.js - This file only contains the context definition
import { createContext, useContext } from "react";

// Export only the context - no components here
export const AuthContext = createContext();

// You can also export a custom hook for easier context consumption
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
