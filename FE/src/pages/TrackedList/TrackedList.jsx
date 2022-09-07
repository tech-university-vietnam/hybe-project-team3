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
  ]);

  const [errorMessage, setErrorMessage] = useState("");

  const PER_PAGE = 7;

  const count = Math.ceil(listOfTrackedMedicineItems.length / PER_PAGE);
  const _DATA = usePagination(listOfTrackedMedicineItems, PER_PAGE);

  const handleChange = (e, p) => {
    setCurrentPage(p);
    _DATA.jump(p);
  };

  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(typeof value === "string" ? value.split(",") : value);
    // - filter the `listOfTrackedMedicineItems` based on the `selectedStatuses`
    // - set the result of the filter to `listOfTrackedMedicineItemsToDisplay`
    // setListOfTrackedMedicineToDisplay(
    //   selectedStatuses.map((selectedStatus) =>
    //     listOfTrackedMedicineItems.filter(
    //       (trackedMedicineItem) => trackedMedicineItem.status === selectedStatus
    //     )
    //   )
    // );
  };

  const getAllTrackedMedicineItems = async () => {
    try {
      const response = await axios.get(url);
      setListOfTrackedMedicineItems(response.data);
    } catch (error) {
      console.log("Error getting list of tracked medicine items", error);
    }
    // setNumberOfTrackedMedicineItems(listOfTrackedMedicineItems.length);
    // setCurrentPage(1);
    // calculateNumberOfPage();
    // handleSlicingDataForPagination();
  };
  //
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
    // - count how many elements in `listOfTrackedMedicineItems` ✅
    // - set that numberOfTrackedMedicineItems ✅
    // - call `calculateNumberOfPage` to set `numberOfPage` ✅
    // - call `handleSlicingDataForPagination` to set list to display for 1st page ✅
    getAllTrackedMedicineItems();
  }, []);

  // WHENEVER USER CLICKS ON ANOTHER PAGE ✅:
  // - call `handlePageChange` to set `currentPage` and slice data at the same time ✅

  // WHENEVER USER CLICKS ON FILTER:
  // - filter the `listOfTrackedMedicineItems` based on the `selectedStatuses`
  // - set the result of the filter to `listOfTrackedMedicineItemsToDisplay`

  // WHENEVER USER CLICKS ON DELETE: ✅
  // - call `handleDeleteMedicineItem` ✅
  // - when the operation is successful, call API to get the updated list of tracked items ✅

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
          medicineItems={_DATA.currentData()}
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
