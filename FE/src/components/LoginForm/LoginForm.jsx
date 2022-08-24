import React, { useState } from "react";
import axios from "axios";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { LoginSchema } from "Utils/validation/LoginSchema";
import { Box, Button, Container, TextField, Typography } from "@mui/material";

// TODO: call backend api to login
// TODO: error handling for incorrect email/password

let loginUrl = "localhost:8000/login";

const LoginForm = (props) => {
  const [loginError, setLoginError] = useState(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(LoginSchema),
  });

  const onSubmit = (data) => {
    axios
      .post(loginUrl, data)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        setLoginError(error);
      });
  };

  return (
    <div>
      <Container
        maxWidth="xs"
        style={{
          display: "grid",
          gridRowGap: "20px",
          padding: "20px",
        }}
      >
        <Box>
          <Typography variant="h6" textAlign="left">
            Welcome back
          </Typography>
          <Typography variant="h4" fontWeight="bold" textAlign="left">
            Login to your account
          </Typography>
        </Box>
        <TextField
          required
          id="email"
          name="email"
          label="Email"
          {...register("email")}
          error={errors.email ? true : false}
        />

        <TextField
          required
          id="password"
          name="password"
          label="Password"
          {...register("password")}
          error={errors.password ? true : false}
        />

        {loginError && (
          <Typography color="red">
            Cannot login to server. Please try again
          </Typography>
        )}

        <Typography
          color="red"
          data-testid="email-error"
          sx={{ display: errors.email?.message ? "inline" : "none" }}
        >
          {errors.email?.message}
        </Typography>
        <Typography
          color="red"
          data-testid="password-error"
          sx={{ display: errors.password?.message ? "inline" : "none" }}
        >
          {errors.password?.message}
        </Typography>

        <Button
          data-testid="login-button-test"
          variant="contained"
          onClick={handleSubmit(onSubmit)}
          sx={{ height: "50px", fontWeight: "bold" }}
        >
          Sign up
        </Button>
        <Typography>Don't have an account? Join free today</Typography>
      </Container>
    </div>
  );
};

LoginForm.propTypes = {};

export default LoginForm;
