import { render, screen } from "@testing-library/react";
import Header from "./Header";

describe("Header tests", () => {
  it("renders the email of the user", () => {
    render(<Header email="test@test.com" />);

    expect(screen.getByText("test@test.com")).toBeInTheDocument();
  });
});
