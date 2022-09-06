import React, { useState } from "react";
import PropTypes from "prop-types";
import TabBar from "../../components/TabBar/TabBar";
import AddItemButton from "../../components/AddItemButton/AddItemButton";
import "./TrackList.css";
import { Button, Pagination } from "@mui/material";
import FilterAltIcon from "@mui/icons-material/FilterAlt";
import MedicineItems from "components/MedicineItems/MedicineItems";

const TrackList = (props) => {
  const [page, setPage] = useState(1);
  const data = Array(10).fill({medicineName: "Panadol", hospitalName: "VinMec", expirationDate: "10/12/2023", status: "LISTED", handleDelete: () => {}});

  // needs to filter data here
  // needs to handle pagination here

  return (
    <div className="dashboard-container">
      <TabBar />
      <div className="content-container">
        <div className="content-header">
          <AddItemButton type="inventory" />
          <Pagination
            count={10}
            variant="outlined"
            page={page}
            onChange={(_, pageNumber) => setPage(pageNumber)}
          />
          <Button>
            <FilterAltIcon />
            Filter
          </Button>
        </div>
        <div className="data-container">
          <MedicineItems medicineItems={data} />
        </div>
        <Pagination
          count={10}
          variant="outlined"
          page={page}
          onChange={(_, pageNumber) => setPage(pageNumber)}
        />
      </div>
    </div>
  );
};

TrackList.propTypes = {};

export default TrackList;
