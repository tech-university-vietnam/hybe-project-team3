import { useForm } from 'react-hook-form';
import { FormControl, InputLabel, Select, MenuItem, Button, Typography, TextField } from '@mui/material';
import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@mui/system';

const RegisterForm = props => {
    const { register, handleSubmit, watch, formState: { errors } } = useForm();
    const onSubmit = data => console.log(data);

    return (
        <>
            <Container
                maxWidth='sm'
                style={{
                    display: "grid",
                    gridRowGap: "30px",
                    padding: "20px"
                }}
            >
                <Typography variant="h4">Create your account</Typography>
                <TextField
                    label='Email'
                    variant='outlined'
                    type='email'
                />
                <TextField
                    label='Password'
                    variant='outlined'
                    type='password'
                />
                <TextField
                    label='Re-type your password'
                    variant='outlined'
                    type='email'
                />
                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Hospital</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        // value={age}
                        label="Hospital"
                    // onChange={handleChange}
                    >
                        <MenuItem value={10}>Ten</MenuItem>
                        <MenuItem value={20}>Twenty</MenuItem>
                        <MenuItem value={30}>Thirty</MenuItem>
                    </Select>
                </FormControl>
                <Button variant="contained">Sign up</Button>
            </Container>

        </>

        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        // <form onSubmit={handleSubmit(onSubmit)}>
        //     {/* register your input into the hook by invoking the "register" function */}
        //     <input defaultValue="test" {...register("example")} />

        //     {/* include validation with required or other standard HTML validation rules */}
        //     <input {...register("exampleRequired", { required: true })} />
        //     {/* errors will return when field validation fails  */}
        //     {errors.exampleRequired && <span>This field is required</span>}

        //     <input type="submit" />
        // </form>
    )
}

RegisterForm.propTypes = {}

export default RegisterForm