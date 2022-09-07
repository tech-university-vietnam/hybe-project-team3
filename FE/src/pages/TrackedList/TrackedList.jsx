import React, { useState } from "react";
import AddItemButton from "../../components/AddItemButton/AddItemButton";
import "./TrackedList.css";
import { Pagination, Alert } from "@mui/material";
import MedicineItems from "components/MedicineItems/MedicineItems";
import Filter from "components/Filter/Filter";
import axios from "axios";
import { useEffect } from "react";
import usePagination from "../../Utils/hooks/pagination";

let url = "http://localhost:8000/tracking-medicines";

const TrackedList = () => {
  const [listOfTrackedMedicineItems, setListOfTrackedMedicineItems] = useState(
    []
  );

  const [currentPage, setCurrentPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState([
    "LISTED",
    "NOT LISTED",
    "FINISHED LISTING",
    "EXPIRED",
  ]);
  const [errorMessage, setErrorMessage] = useState("");
  const [filteredMedicines, setFilteredMedicines] = useState([]);

  const PER_PAGE = 7;

  const count = Math.ceil(filteredMedicines.length / PER_PAGE);
  const filteredMedicineItems = usePagination(filteredMedicines, PER_PAGE);

  const handleChange = (e, p) => {
    setCurrentPage(p);
    filteredMedicineItems.jump(p);
  };

  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(typeof value === "string" ? value.split(",") : value);
    setFilteredMedicines(
      listOfTrackedMedicineItems.filter((medicineItem) =>
        selectedStatuses.map((status) => medicineItem.status === status)
      )
    );
  };

  const getAllTrackedMedicineItems = async () => {
    try {
      const response = await axios.get(url);
      setListOfTrackedMedicineItems(response.data);
    } catch (error) {
      console.log("Error getting list of tracked medicine items", error);
    }
  };
  const handleDeleteMedicineItem = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/tracking-medicine/${id}`);
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

  useEffect(() => {
    setFilteredMedicines(
      listOfTrackedMedicineItems.filter((medicineItem) =>
        selectedStatuses.map((status) => medicineItem.status === status)
      )
    );
  }, [listOfTrackedMedicineItems, selectedStatuses]);

  return (
    <div className="content-container">
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <div className="content-header">
        <AddItemButton type="tracked list" />
        <Pagination
          count={count}
          size="large"
          page={currentPage}
          variant="outlined"
          shape="rounded"
          onChange={handleChange}
        />
        <Filter
          statuses={["LISTED", "NOT LISTED", "FINISHED LISTING"]}
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
        onChange={handleChange}
      />
    </div>
  );
};

TrackedList.propTypes = {};

export default TrackedList;
