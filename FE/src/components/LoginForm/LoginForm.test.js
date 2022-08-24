import { fireEvent, render, screen } from "@testing-library/react";
import LoginForm from "./LoginForm";

describe("LoginForm", () => {
  it("loads the email and password input fields", () => {
    render(<LoginForm />);

    expect(screen.getByText("Email")).toBeInTheDocument();
    expect(screen.getByText("Password")).toBeInTheDocument();
  });

  it("loads the login button", () => {
    render(<LoginForm />);

    expect(screen.getByRole("button")).toBeInTheDocument();
  });
});
