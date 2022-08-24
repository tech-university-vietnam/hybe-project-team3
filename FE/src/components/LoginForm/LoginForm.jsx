import React from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { LoginSchema } from "Utils/validation/LoginSchema";
import { Box, Button, Container, TextField, Typography } from "@mui/material";

// TODO: call backend api to login
// TODO: error handling for incorrect email/password

const LoginForm = (props) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(LoginSchema),
  });

  const onSubmit = (data) => console.log("submit data is", data);

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

        <Typography
          color="red"
          data-testid="email-error"
          sx={{ visibility: errors.email?.message ? "visible" : "hidden" }}
        >
          {errors.email?.message}
        </Typography>
        <Typography
          color="red"
          data-testid="password-error"
          sx={{ visibility: errors.password?.message ? "visible" : "hidden" }}
        >
          {errors.password?.message}
        </Typography>

        <Button
          data-testid="button-test"
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
