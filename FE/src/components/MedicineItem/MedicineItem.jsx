import { React, useEffect, useState } from "react";
import PropTypes from "prop-types";
import {
  Card,
  CardContent,
  Chip,
  Grid,
  IconButton,
  Typography,
} from "@mui/material";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";

const MedicineItem = ({
  medicineName = "Panadol",
  hospitalName = "VinMec",
  expirationDate = "10/12/2023",
  status = "LISTED",
  handleDelete = () => {},
}) => {
  const [badgeColor, setBadgeColor] = useState(() => {
    if (status === "LISTED") {
      return "primary";
    } else if (status === "NOT LISTED") {
      return "secondary";
    } else {
      return "success";
    }
  });

  useEffect(() => {
    if (status === "LISTED") {
      setBadgeColor("primary");
    } else if (status === "NOT LISTED") {
      setBadgeColor("secondary");
    } else {
      setBadgeColor("success");
    }
  }, [status]);

  return (
    <Card sx={{ width: "70rem", marginBottom: "30px" }}>
      <CardContent>
        <Grid
          container
          sx={{ alignItems: "center", justifyContent: "space-between" }}
        >
          <Grid xs={3}>
            <Typography>{medicineName}</Typography>
          </Grid>
          <Grid xs={3}>
            <Typography>{hospitalName}</Typography>
          </Grid>
          <Grid xs={3}>
            <Typography>{expirationDate}</Typography>
          </Grid>
          <Grid xs={2}>
            <Chip
              label={status}
              color={badgeColor}
              sx={{ fontWeight: "bold" }}
            />
          </Grid>
          <Grid>
            <IconButton onClick={handleDelete}>
              <DeleteSweepIcon sx={{ color: "red" }} />
            </IconButton>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

MedicineItem.propTypes = {
  hospitalName: PropTypes.string,
  medicineName: PropTypes.string,
  expirationDate: PropTypes.string,
  status: PropTypes.string,
  handleDelete: PropTypes.func,
};

export default MedicineItem;
