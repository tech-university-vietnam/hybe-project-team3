import { React, useState } from "react";
import PropTypes from "prop-types";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Checkbox,
  ListItemText,
  Select,
  OutlinedInput,
} from "@mui/material";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const Filter = ({
  statuses,
  selectedStatuses,
  handleChange,
}) => {

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">Status filter</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={selectedStatuses}
          onChange={handleChange}
          input={<OutlinedInput label="Status filter" />}
          renderValue={(selected) => selected.join(", ")}
          MenuProps={MenuProps}
        >
          {statuses.map((status) => (
            <MenuItem key={status} value={status}>
              <Checkbox checked={selectedStatuses.indexOf(status) > -1} />
              <ListItemText primary={status} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};

Filter.propTypes = {
  statuses: PropTypes.arrayOf(PropTypes.string),
  selectedStatuses: PropTypes.arrayOf(PropTypes.string),
  handleChange: PropTypes.func,
};

export default Filter;
