import { render, screen } from "@testing-library/react";
import LoginForm from "./LoginForm";

test("loads the email and password input fields", () => {
  render(<LoginForm />);

  const emailInputField = screen.getByLabelText(/email/i);
  const passwordInputField = screen.getByLabelText(/password/i);

  expect(emailInputField).toBeInTheDocument();
  expect(passwordInputField).toBeInTheDocument();
});

// test("shows error when the email is NOT correct", () => {
//   render(<LoginForm />);
// });

// test("shows error when the email field is NOT filled", () => {
//   render(<LoginForm />);
// });

// test("shows error when the password field is NOT filled", () => {
//   render(<LoginForm />);
// });
