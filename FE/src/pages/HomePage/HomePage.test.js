import { render, screen } from "@testing-library/react";
import { HomePage } from "./HomePage";

test("renders learn react link", () => {
  render(<HomePage />);
  const welcomeMsg = screen.getByText(/HYBE/);
  expect(welcomeMsg).toBeInTheDocument();
});
T