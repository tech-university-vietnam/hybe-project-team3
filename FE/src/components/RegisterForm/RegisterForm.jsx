import { Controller, useForm } from "react-hook-form";
import {
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { Container } from "@mui/system";
import { RegisterSchema } from "../../Utils/validation/RegisterSchema";
import { yupResolver } from "@hookform/resolvers/yup";
import { postRegister } from "Utils/api/authentication";
import axios from "axios";
import { getHospitals } from "Utils/api/hospitals";

const RegisterForm = () => {
  const [error, setError] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [hospitals, setHospitals] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(RegisterSchema),
  });

  const getHospitalList = async () => {
    await getHospitals()
      .then(response => {
        setHospitals(response);
        setIsLoading(false);
      })
      .catch(_ => {
        setError(true);
        setStatusMessage("Could not get hospital list. Please try again");
        setIsLoading(false);
      })
  };

  const onSubmit = async (data) => {
    try {
      await postRegister(data);
      setStatusMessage("success");
    } catch {
      setError(true);
      setStatusMessage("Could not sign up. Please submit again");
    }
  };

  useEffect(() => {
    getHospitalList();
  }, []);

  if (isLoading) {
    return <div>Loading register form please wait</div>;
  } else {
    return (
      <>
        <Container
          maxWidth="xs"
          style={{
            display: "grid",
            gridRowGap: "20px",
            padding: "20px",
          }}
        >
          <Typography variant="h4" fontWeight="bold" textAlign="left">
            Create your account
          </Typography>
          <TextField
            required
            id="email"
            name="email"
            label="Email"
            fullWidth
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
            data-testid="password"
            {...register("password")}
            error={errors.password ? true : false}
            helperText={errors.password?.message}
          />
          <TextField
            required
            id="confirmPassword"
            name="confirmPassword"
            label="Re-type your password"
            type="password"
            data-testid="confirmPassword"
            {...register("confirmPassword")}
            error={errors.confirmPassword ? true : false}
            helperText={errors.confirmPassword?.message}
          />
          <Controller
            control={control}
            name="hospital"
            render={({ field: { onChange, value } }) => (
              <FormControl
                fullWidth
                required
                {...register("hospital")}
                error={errors.hospital ? true : false}
              >
                <InputLabel id="hospitalLabel">Hospital</InputLabel>
                <Select
                  data-testid="select-hospital"
                  labelId="hospitalLabel"
                  label="Hospital"
                  id="hospital"
                  value={value}
                  onChange={onChange}
                  defaultValue=""
                >
                  {hospitals.map((hospital) => (
                    <MenuItem key={hospital.id} value={hospital.id}>
                      {hospital.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          />
          <Typography color="red">{errors.hospital?.message}</Typography>

          {error && (
            <Typography align="center" color="red">
              {statusMessage}
            </Typography>
          )}

          {statusMessage === "success" ? (
            <Typography align="center">
              Registered successfully 🎉! <a href="/login">Log in</a> to your
              account.
            </Typography>
          ) : (
            <Button
              disabled={hospitals.length === 0}
              variant="contained"
              onClick={handleSubmit(onSubmit)}
              sx={{ fontWeight: "bold", height: "56px" }}
            >
              Sign up
            </Button>
          )}
        </Container>
      </>
    );
  }
};

RegisterForm.propTypes = {};

export default RegisterForm;
