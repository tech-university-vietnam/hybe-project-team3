import React, { useState } from "react";
import PropTypes from "prop-types";
import TabBar from "../../components/TabBar/TabBar";
import AddItemButton from "../../components/AddItemButton/AddItemButton";
import "./Dashboard.css";
import MedicineItem from "components/MedicineItem/MedicineItem";
import { Pagination } from "@mui/material";
import Filter from "components/Filter/Filter";

const Dashboard = (props) => {
  const [page, setPage] = useState(1);
  const data = Array(10).fill("item");
  console.log(data);

  const [selectedStatus, SetSelectedStatus] = useState([]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    SetSelectedStatus(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

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
            onChange={(event, pageNumber) => setPage(pageNumber)}
          />
          <Filter
            statuses={["LISTED", "NOT LISTED", "FINISHED LISTING"]}
            selectedStatuses={selectedStatus}
            handleChange={handleChange}
          />
        </div>
        <div className="data-container">
          {data.map((item) => (
            <MedicineItem name="Sinovac" exp="20/10/2030" />
          ))}
        </div>
        <Pagination
          count={10}
          variant="outlined"
          page={page}
          onChange={(event, pageNumber) => setPage(pageNumber)}
        />
      </div>
    </div>
  );
};

Dashboard.propTypes = {};

export default Dashboard;
