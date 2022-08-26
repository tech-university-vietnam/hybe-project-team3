import {
  userEvent,
  act,
  fireEvent,
  render,
  screen,
} from "@testing-library/react";
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

  it("shows the async login error when username or password is NOT correct", async () => {
    render(<LoginForm />);

    const inputEl = screen.getByLabelText(/email/i);
    const passwordEl = screen.getByLabelText(/password/i);

    fireEvent.change(inputEl, { target: { value: "a@a.com" } });
    fireEvent.change(passwordEl, { target: { value: "a" } });

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });

    expect(
      screen.getByText("Cannot login to server. Please try again")
    ).toBeInTheDocument();
  });

  it("shows email error when no email is in the email input", async () => {
    render(<LoginForm />);

    const passwordEl = screen.getByLabelText(/password/i);
    fireEvent.change(passwordEl, { target: { value: "a" } });

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });

    expect(screen.getByText("Email is required")).toBeInTheDocument();
  });

  it("shows password error when no password is in the password input", async () => {
    render(<LoginForm />);

    const inputEl = screen.getByLabelText(/email/i);
    fireEvent.change(inputEl, { target: { value: "a@a.com" } });

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });

    expect(screen.getByText("Password is required")).toBeInTheDocument();
  });

  it("shows email and password errors when no value is in both inputs", async () => {
    render(<LoginForm />);

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });
    expect(screen.getByText("Email is required")).toBeInTheDocument();
    expect(screen.getByText("Password is required")).toBeInTheDocument();
  });

  it("shows error for invalid email format", async () => {
    render(<LoginForm />);

    const inputEl = screen.getByLabelText(/email/i);
    fireEvent.change(inputEl, { target: { value: "a" } });

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });
    expect(screen.getByText("Email is invalid")).toBeInTheDocument();
  });
});
