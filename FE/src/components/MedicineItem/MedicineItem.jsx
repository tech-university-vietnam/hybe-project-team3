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
import moment from "moment";

const badgeColorMap = {
  Listed: "primary",
  "Not listed": "secondary",
  "Finished listing": "success",
  Available: "primary",
  Unavailable: "secondary",
  Resolved: "success",
};

const MedicineItem = ({
  id,
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
            <Typography>
              {moment(expirationDate).format("YYYY-MM-DD")}
            </Typography>
          </Grid>
          <Grid xs={2}>
            <Chip
              onClick={() => console.log("clicking status")}
              label={status}
              color={badgeColor}
              sx={{ fontWeight: "bold" }}
            />
          </Grid>
          <Grid>
            <IconButton
              onClick={() => {
                handleDelete(id);
              }}
            >
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
