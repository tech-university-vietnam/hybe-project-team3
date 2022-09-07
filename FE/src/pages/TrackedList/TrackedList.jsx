import React, { useState, useEffect, useMemo } from "react";
import AddItemButton from "../../components/AddItemButton/AddItemButton";
import "./TrackedList.css";
import { Pagination, Alert } from "@mui/material";
import MedicineItems from "components/MedicineItems/MedicineItems";
import Filter from "components/Filter/Filter";
import axios from "axios";
import usePagination from "../../Utils/hooks/pagination";
import "./TrackedList.css";

const getMedicinesUrl = "http://localhost:8000/tracking-medicines";
const deleteMedicineUrl = "http://localhost:8000/tracking-medicine";

const TrackedList = () => {
  const [listOfTrackedMedicineItems, setListOfTrackedMedicineItems] = useState(
    []
  );

  const [currentPage, setCurrentPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState([
    "LISTED",
    "Not listed",
    "FINISHED LISTING",
    "EXPIRED",
  ]);
  const [errorMessage, setErrorMessage] = useState("");
  // const [filteredMedicines, setFilteredMedicines] = useState([]);

  const filteredMedicines = useMemo(() => {
    return listOfTrackedMedicineItems.filter((medicineItem) =>
      selectedStatuses.includes(medicineItem.status)
    );
  }, [listOfTrackedMedicineItems, selectedStatuses]);

  const PER_PAGE = 7;

  const count = Math.ceil(filteredMedicines.length / PER_PAGE);
  const filteredMedicineItems = usePagination(filteredMedicines, PER_PAGE);

  const handlePageChange = (e, p) => {
    setCurrentPage(p);
    filteredMedicineItems.jump(p);
  };

  const handleListChange = async () => {
    try {
      await getAllTrackedMedicineItems();
    } catch (error) {
      console.log(
        "Error getting updated tracked medicines list in handleListChange",
        error
      );
      setErrorMessage(error.detail.msg);
    }
  };

  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(typeof value === "string" ? value.split(",") : value);
  };

  const getAllTrackedMedicineItems = async () => {
    try {
      const response = await axios.get(getMedicinesUrl, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setListOfTrackedMedicineItems(response.data);
    } catch (error) {
      console.log(
        "Error getting list of tracked medicines list in getAllTrackedMedicineItems",
        error
      );
      setErrorMessage(error.detail.msg);
    }
  };
  const handleDeleteMedicineItem = async (id) => {
    try {
      await axios.delete(`${deleteMedicineUrl}/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      await getAllTrackedMedicineItems();
    } catch (error) {
      console.log("Error deleting item", error);
      setErrorMessage(error.detail.msg);
    }
  };

  useEffect(() => {
    // ** when the page first loads**:
    // - fetch data for tracked medicine items ✅
    // - set that data into `listOfTrackedMedicineItems` ✅
    // - filter the data into `filteredMedicines`
    getAllTrackedMedicineItems();
  }, []);

  return (
    <div className="content-container">
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <div className="content-header">
        <AddItemButton
          type="tracked list"
          handleListChange={handleListChange}
        />
        <Pagination
          count={count}
          size="large"
          page={currentPage}
          variant="outlined"
          shape="rounded"
          onChange={handlePageChange}
        />
        <Filter
          statuses={["LISTED", "Not listed", "FINISHED LISTING"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className="data-container">
        <MedicineItems
          medicineItems={filteredMedicineItems.currentData()}
          handleDelete={handleDeleteMedicineItem}
        />
      </div>
      <Pagination
        count={count}
        size="large"
        page={currentPage}
        variant="outlined"
        shape="rounded"
        onChange={handlePageChange}
      />
    </div>
  );
};

TrackedList.propTypes = {};

export default TrackedList;
