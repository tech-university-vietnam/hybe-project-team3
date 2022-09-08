import React, { useState } from "react";
import axios from "axios";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { LoginSchema } from "Utils/validation/LoginSchema";
import { useNavigate } from "react-router-dom";
import { Box, Button, Container, TextField, Typography } from "@mui/material";
import useAuth from "../../Utils/hooks/auth.js";

// TODO: call backend api to login
// TODO: error handling for incorrect email/password

const LoginForm = () => {
  const [loginError, setLoginError] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(LoginSchema),
  });

  const onSubmit = async (data) => {
    let success = true;
    await login(data)
      .catch((error) => {
        success = false;
        setLoginError(error.data.msg);
      });
    console.log(success)
    if (success) {
      navigate("/");
    }
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
          helperText={errors.email?.message}
        />

        <TextField
          required
          id="password"
          name="password"
          label="Password"
          type="password"
          {...register("password")}
          error={errors.password ? true : false}
          helperText={errors.password?.message}
        />

        {loginError && (
          <>
            <Typography color="red" data-testid="login-error">
              {loginError}
            </Typography>
          </>
        )}

        <Button
          variant="contained"
          onClick={handleSubmit(onSubmit)}
          sx={{ height: "50px", fontWeight: "bold" }}
        >
          Login
        </Button>
        <Typography>Don't have an account? <a href="/register">Join</a> free today</Typography>
      </Container>
    </div>
  );
};

LoginForm.propTypes = {};

export default LoginForm;
