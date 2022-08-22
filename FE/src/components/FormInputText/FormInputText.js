import { TextField } from "@mui/material";
import { Controller } from "react-hook-form";
import React from "react";

export const FormInputText = ({ name, control, label, type }) => {
    return (
        <Controller
            name={name}
            control={control}
            render={({ field: { onChange, value } }) => (
                <TextField
                    onChange={onChange}
                    value={value}
                    label={label}
                    type={type}
                    variant='outlined'
                />
            )}
        />
    );
};