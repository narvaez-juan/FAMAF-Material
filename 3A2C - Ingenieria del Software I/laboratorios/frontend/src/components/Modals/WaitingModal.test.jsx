import React from "react";
import { render, screen } from "@testing-library/react";
import WaitingModal from "./WaitingModal";

describe("WaitingModal", () => {
  test("renders waiting text for REVEAL effect", () => {
    render(<WaitingModal targetName="fran" effect="REVEAL" />);
    expect(screen.getByText(/Waiting for fran/i)).toBeInTheDocument();
    expect(
      screen.getByText(/is choosing which secret to reveal/i)
    ).toBeInTheDocument();
  });

  test("renders waiting text for HIDE effect", () => {
    render(<WaitingModal targetName="fran" effect="HIDE" />);
    expect(screen.getByText(/Waiting for fran/i)).toBeInTheDocument();
    expect(
      screen.getByText(/is choosing a secret to hide/i)
    ).toBeInTheDocument();
  });

  test("renders waiting text for STEAL effect", () => {
    render(<WaitingModal targetName="fran" effect="STEAL" />);
    expect(screen.getByText(/Waiting for fran/i)).toBeInTheDocument();
    expect(
      screen.getByText(/is choosing a secret to steal/i)
    ).toBeInTheDocument();
  });

  test("renders minimal heading when no effect provided", () => {
    render(<WaitingModal targetName="fran" />);
    expect(screen.getByText(/Waiting for fran/i)).toBeInTheDocument();
  });
});
