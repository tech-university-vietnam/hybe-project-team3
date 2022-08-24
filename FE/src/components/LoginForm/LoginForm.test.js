import { fireEvent, render, screen } from "@testing-library/react";
import LoginForm from "./LoginForm";

test("loads the email and password input fields", () => {
  render(<LoginForm />);

  expect(screen.getByText("Email")).toBeInTheDocument();
  expect(screen.getByText("Password")).toBeInTheDocument();
});

test("shows error where the email is NOT correct", () => {
  render(<LoginForm />);
  const emailInputField = screen.getByLabelText(/email/i);
  const passwordInputField = screen.getByLabelText(/password/i);

  fireEvent.change(emailInputField, { target: { value: "a" } });
  fireEvent.change(passwordInputField, { target: { value: "a" } });

  fireEvent.click(screen.getByRole("button"));
  expect(screen.getByTestId("email-error")).toBeInTheDocument();
});

test("shows email error when the email field is NOT filled", () => {
  render(<LoginForm />);
  const passwordInputField = screen.getByLabelText(/password/i);
  fireEvent.change(passwordInputField, { target: { value: "a" } });

  fireEvent.click(screen.getByTestId("login-button-test"));
  expect(screen.getByTestId("password-error")).toBeInTheDocument();
});

test("shows password error when the password field is NOT filled", () => {
  render(<LoginForm />);
  const emailInputField = screen.getByLabelText(/email/i);
  fireEvent.change(emailInputField, { target: { value: "a@mail.com" } });

  fireEvent.click(screen.getByTestId("login-button-test"));
  expect(screen.getByTestId("email-error")).toBeInTheDocument();
});
