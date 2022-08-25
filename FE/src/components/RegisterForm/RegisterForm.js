import { Controller, useForm } from 'react-hook-form';
import { Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import React from 'react';
import { Container } from '@mui/system';
import { RegisterSchema } from 'validation/RegisterSchema';
import { yupResolver } from '@hookform/resolvers/yup';

const RegisterForm = props => {
    const {
        register,
        control,
        handleSubmit,
        formState: { errors }
    } = useForm({
        resolver: yupResolver(RegisterSchema)
    })

    const onSubmit = data => console.log(data);

    const getHospitalList = () => {
        const options = [
            {
                label: "Dropdown Option 1",
                value: "1",
            },
            {
                label: "Dropdown Option 2",
                value: "2",
            },
        ];
        return options;
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
                    id="passwordId"
                    name="password"
                    label="Password"
                    type="password"
                    
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
                    {...register('confirmPassword')}
                    error={errors.confirmPassword ? true : false}
                />
                <Typography color="red">
                    {errors.confirmPassword?.message}
                </Typography>
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
                                labelId="hospitalLabel"
                                label="Hospital"
                                id="hospital"
                                value={value}
                                onChange={onChange}
                                defaultValue=""
                            >
                                {getHospitalList().map(hospital =>
                                    <MenuItem key={hospital.value} value={hospital.value}>{hospital.label}</MenuItem>
                                )}
                            </Select>
                        </FormControl>)}
                />
                <Typography color="red">
                    {errors.hospital?.message}
                </Typography>
                <Button
                    variant="contained"
                    onClick={handleSubmit(onSubmit)}>
                    Sign up
                </Button>
            </Container>
        </>
    )
}

RegisterForm.propTypes = {}

export default RegisterForm