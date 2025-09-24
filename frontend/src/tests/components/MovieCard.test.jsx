import React from "react";
import { render, screen } from "@testing-library/react";
import { it, expect, describe } from "vitest";
import MovieCard from "../../components/MovieCard";
import { MovieProvider } from "../../contexts/MovieContext";
import { MemoryRouter } from "react-router-dom";

describe("Movie Card Component", () => {
  it("Should show movie card when data has been passed", () => {
    const fakeMovie = { id: 1, title: "Iron Man 3", release_date: "2020" };

    render(
      <MemoryRouter>
        <MovieProvider>
          <MovieCard movie={fakeMovie} />
        </MovieProvider>
      </MemoryRouter>
    );

    const titleElement = screen.getByText("Iron Man 3");
    expect(titleElement).toBeInTheDocument();
  });

  it("Should not render data to moviecard when the data hasnt been passed"),
    () => {
      render(
        <MemoryRouter>
          <MovieProvider>
            <MovieCard />
          </MovieProvider>
        </MemoryRouter>
      );

      // Expect the title NOT to be found
      const titleElement = screen.queryByText("Iron Man 3");
      expect(titleElement).toBeNull(); // or use expect(titleElement).not.toBeInTheDocument()
    };
});
