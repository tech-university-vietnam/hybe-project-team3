import React from "react";
import { Chip } from "@mui/material";


const badgeColorMap = {
  Listed: "primary",
  "Not listed": "secondary",
  "Finished listing": "success",
  Available: "primary",
  Unavailable: "secondary",
  Resolved: "success",
};

const ChipStatus = ({status, openPopup, id, name}) => (
  <Chip
    onClick={
      ["Resolved", "Available", "Finished listing"].includes(status)
        ? () => openPopup({ id, status, name })
        : () => { }
    }
    label={status}
    color={badgeColorMap[status]}
    sx={{ fontWeight: "bold" }}
  />
)

export default ChipStatus