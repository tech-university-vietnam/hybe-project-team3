import React from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import { useFormContext, Controller } from "react-hook-form";

export const FormInputDropdown = ({ name, control, label, options }) => {

    const generateSelectOptions = () => {
        return options.map((option) => {
            return (
                <MenuItem key={option.value} value={option.value}>
                    {option.label}
                </MenuItem>
            );
        });
    };

    return <Controller
        control={control}
        name={name}
        render={({ field: { onChange, value } }) => (
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">{label}</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    label={label}
                    onChange={onChange}
                    value={value}
                >
                    {generateSelectOptions()}
                </Select>
            </FormControl>
        )}
    />
};