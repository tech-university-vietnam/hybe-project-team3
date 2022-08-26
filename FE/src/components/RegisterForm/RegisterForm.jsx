import { Controller, useForm } from 'react-hook-form';
import { Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { Container } from '@mui/system';
import { RegisterSchema } from 'validation/RegisterSchema';
import { yupResolver } from '@hookform/resolvers/yup';
import axios from 'axios';

const RegisterForm = props => {
    const [message, setMessage] = useState("");
    const [hospitals, setHospitals] = useState();
    const [isLoading, setIsLoading] = useState(true);
    const {
        register,
        control,
        handleSubmit,
        formState: { errors }
    } = useForm({
        resolver: yupResolver(RegisterSchema)
    })

    useEffect(() => {
        const fetchAPI = async () => {
            setIsLoading(true);
            const response = await getHospitalList();
            setHospitals(response);
            setIsLoading(false);
        }
        fetchAPI();
    }, [])

    const onSubmit = data => {
        async function fetchAPI() {
            let url = 'http://localhost:8000/register'
            const response = await axios.post(url, {
                "email": data.email,
                "password": data.password,
                "work_for": data.hospital
            })
            if (response.status === 201) {
                setMessage("success");
            } else {
                setMessage("Error.")
            }
        }

        fetchAPI()
    }

    const getHospitalList = async () => {
        let url = 'http://localhost:8000/hospitals'
        const response = await axios.get(url)
        if (response.status === 200) {
            return response.data.hospitals;
        } else {
            return null;
        }
    }

    return (
        <>
            <Container
                maxWidth='xs'
                style={{
                    display: "grid",
                    gridRowGap: "20px",
                    padding: "20px"
                }}
            >
                <Typography variant="h4">Create your account</Typography>
                <TextField
                    required
                    id="email"
                    name="email"
                    label="Email"
                    fullWidth
                    // margin="dense"
                    {...register('email')}
                    error={errors.email ? true : false}
                />
                <Typography color="red">
                    {errors.email?.message}
                </Typography>
                <TextField
                    required
                    id="password"
                    name="password"
                    label="Password"
                    type="password"
                    data-testid="password"
                    {...register('password')}
                    error={errors.password ? true : false}
                />
                <Typography color="red">
                    {errors.password?.message}
                </Typography>
                <TextField
                    required
                    id="confirmPassword"
                    name="confirmPassword"
                    label="Re-type your password"
                    type="password"
                    data-testid="confirmPassword"
                    {...register('confirmPassword')}
                    error={errors.confirmPassword ? true : false}
                />
                <Typography color="red">
                    {errors.confirmPassword?.message}
                </Typography>
                {isLoading ? <></> :
                    hospitals === null ?
                        <Typography>Cannot get the hospital list, please try again later.</Typography> :
                        <Controller
                            control={control}
                            name="hospital"
                            render={({ field: { onChange, value } }) => (
                                <FormControl
                                    fullWidth
                                    required
                                    {...register('hospital')}
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
                                        {hospitals.map(hospital =>
                                            <MenuItem
                                                key={hospital.id}
                                                value={hospital.id}>
                                                {hospital.name}
                                            </MenuItem>
                                        )}
                                    </Select>
                                </FormControl>)}
                        />
                }
                <Typography color="red">
                    {errors.hospital?.message}
                </Typography>
                {hospitals === null ? <></> :
                    <Button
                        variant="contained"
                        onClick={handleSubmit(onSubmit)}>
                        Sign up
                    </Button>
                }

                {message === "success" ?
                    <Typography align='center'>Registered successfully! <a href="/login">Log in</a> to your account.</Typography> :
                    <Typography align='center'>{message}</Typography>
                }
            </Container>
        </>
    )
}

RegisterForm.propTypes = {}

export default RegisterForm