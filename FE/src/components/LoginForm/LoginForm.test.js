import { render, screen } from "@testing-library/react";
import LoginForm from "./LoginForm";

test("loads the email and password input fields", () => {
  render(<LoginForm />);

  expect(screen.getByText("Email")).toBeInTheDocument();
  expect(screen.getByText("Password")).toBeInTheDocument();
});

// test("shows error where the email is NOT correct", () => {
//   render(<LoginForm />);
//   const emailInputField = screen.getByLabelText(/email/i);
//   const passwordInputField = screen.getByLabelText(/password/i);

//   fireEvent.change(emailInputField, { target: { value: "a" } });
//   fireEvent.change(passwordInputField, { target: { value: "a" } });

//   fireEvent.click(screen.getByRole("button"));
//   expect(screen.getByTestId("email-error")).not.toBeVisible();
// });

// test("shows email error when the email field is NOT filled", () => {
//   render(<LoginForm />);

//   const passwordInputField = screen.getByLabelText(/password/i);
//   fireEvent.change(passwordInputField, { target: { value: "a" } });

//   fireEvent.click(screen.getByTestId("button-test"));

//   expect(screen.getByTestId("password-error")).toBeVisible();
//   expect(screen.queryByTestId("email-error")).not.toBeVisible();
// });

// test("shows password error when the password field is NOT filled", () => {
//   render(<LoginForm />);
// });
