/* eslint-disable testing-library/no-unnecessary-act */
import { fireEvent, render, screen, act, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import RegisterForm from "./RegisterForm";

test("loads the input fields and the button", () => {
    render(<RegisterForm />);
    expect(screen.getByText("Email")).toBeInTheDocument();
    expect(screen.getByText("Password")).toBeInTheDocument();
    expect(screen.getByText("Hospital")).toBeInTheDocument();
    expect(screen.getByText("Re-type your password")).toBeInTheDocument();
    expect(screen.getByRole("button", {
        name: "Sign up"
    })).toBeInTheDocument()
});

test("required validation", async () => {
    render(<RegisterForm />)
    const signUpButton = screen.getByRole("button", {
        name: "Sign up"
    });
    await act(async () => {
        fireEvent.click(signUpButton);
    });

    expect(screen.getByText('Email is required')).toBeInTheDocument()
    expect(screen.getByText('Password is required')).toBeInTheDocument()
    expect(screen.getByText('Confirm password is required')).toBeInTheDocument()
    expect(screen.getByText('Hospital is required')).toBeInTheDocument()
})

test("email validation", async () => {
    render(<RegisterForm />)

    const emailInput = screen.getByRole("textbox", {
        name: "Email"
    })
    const signUpButton = screen.getByRole("button", {
        name: "Sign up"
    });

    const emails = ['hello', 'hello@', 'hello.com', 'hello@c']

    for (const email of emails) {
        userEvent.type(emailInput, email)
        await act(async () => {
            fireEvent.click(signUpButton)
        });
        expect(screen.getByText('Email is invalid')).toBeInTheDocument()
        userEvent.clear(emailInput)
    }
})

test('password validation', async () => {
    render(<RegisterForm />)

    const passwordInput = screen.getByTestId("password").querySelector("input");
    const signUpButton = screen.getByRole("button", {
        name: "Sign up"
    });

    const passwords = ['1234', 'helloimpltd', 'helloimpltd1234', 'HELLOIMPLTD', 'helloimPLTD']

    for (const password of passwords) {
        userEvent.type(passwordInput, password)
        await act(async () => {
            fireEvent.click(signUpButton)
        });
        await screen.findByText('Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and One Special Case Character');
        userEvent.clear(passwordInput)
    }
})

test('confirm password validation', async () => {
    render(<RegisterForm />)

    const passwordInput = screen.getByTestId("password").querySelector("input");
    const confirmPasswordInput = screen.getByTestId("confirmPassword").querySelector("input");
    const signUpButton = screen.getByRole("button", {
        name: "Sign up"
    });

    const password = '123456'
    const confirmPassword = '123'

    userEvent.type(passwordInput, password);
    userEvent.type(confirmPasswordInput, confirmPassword);

    await act(async () => {
        fireEvent.click(signUpButton)
    });

    expect(screen.getByText('Confirm password does not match')).toBeInTheDocument()
})