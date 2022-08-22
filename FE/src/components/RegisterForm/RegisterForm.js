import { useForm } from 'react-hook-form';
import { Button, Typography } from '@mui/material';
import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@mui/system';
import { FormInputText } from 'components/FormInputText/FormInputText';
import { FormInputDropdown } from 'components/FormInputDropdown/FormInputDropdown';

const RegisterForm = props => {
    const { control, handleSubmit } = useForm({
        defaultValues: {
            email: '',
            password: '',
            passwordCheck: '',
            hospital: ''
        }
    }
    );
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
                maxWidth='sm'
                style={{
                    display: "grid",
                    gridRowGap: "30px",
                    padding: "20px"
                }}
            >
                <Typography variant="h4">Create your account</Typography>
                <FormInputText
                    name="email"
                    label="Email"
                    type="email"
                    control={control}
                />
                <FormInputText
                    name="password"
                    label="Password"
                    type="password"
                    control={control}
                />
                <FormInputText
                    name="passwordCheck"
                    label="Re-type your password"
                    type="password"
                    control={control}
                />
                <FormInputDropdown
                    name="hospital"
                    label="Hospital"
                    control={control}
                    options={getHospitalList()}
                />
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