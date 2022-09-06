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

const badgeColorMap = {
  LISTED: "primary",
  "NOT LISTED": "secondary",
  "FINISHED LISTING": "success",
};

const MedicineItem = ({
  medicineName,
  hospitalName,
  expirationDate,
  status,
  handleDelete,
}) => {
  const [badgeColor, setBadgeColor] = useState(() => badgeColorMap[status]);

  useEffect(() => {
    setBadgeColor(badgeColorMap[status]);
  }, [status, badgeColor]);

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
