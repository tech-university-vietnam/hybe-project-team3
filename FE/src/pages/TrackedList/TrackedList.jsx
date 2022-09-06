import React, { useState } from "react";
import AddItemButton from "../../components/AddItemButton/AddItemButton";
import "./TrackedList.css";
import { Pagination } from "@mui/material";
import MedicineItems from "components/MedicineItems/MedicineItems";
import Filter from "components/Filter/Filter";

const TrackedList = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState([]);

  const data = Array(10).fill({
    medicineName: "Panadol",
    hospitalName: "VinMec",
    expirationDate: "10/12/2023",
    status: "LISTED",
    handleDelete: () => {},
  });

  // needs to filter data here
  // needs to handle pagination here

  const handlePageChange = (_, pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(
      typeof value === 'string' ? value.split(',') : value,
    );
  }

  return (
    <div className="content-container">
      <div className="content-header">
        <AddItemButton type="tracked list" />
        <Pagination
          count={10}
          variant="outlined"
          page={currentPage}
          onChange={handlePageChange}
        />
        <Filter
          statuses={["LISTED", "NOT LISTED", "FINISHED LISTING"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className="data-container">
        <MedicineItems medicineItems={data} />
      </div>
      <Pagination
        count={10}
        variant="outlined"
        page={currentPage}
        onChange={handlePageChange}
      />
    </div>
  );
};

TrackedList.propTypes = {};

export default TrackedList;
