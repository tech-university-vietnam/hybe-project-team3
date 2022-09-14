import React, { useState, useEffect, useMemo } from "react";
import AddItemButton from "../../components/AddTrackingItemButton/AddTrackingItemButton";
import styles from "./TrackedList.module.css";
import { Alert, Chip } from "@mui/material";
import Filter from "components/Filter/Filter";
import {
  deleteTrackingMedicine,
  getBuyingHospital,
  getTrackingMedicines,
} from "Utils/api/medicine";
import FinishedListingPopup from "components/TrackedListPopup/FinishedListingPopup";
import DataTable from "components/DataTable/DataTable";
import moment from "moment/moment";
import ChipStatus from "components/ChipStatus/ChipStatus";

const badgeColorMap = {
  Listed: "primary",
  "Not listed": "secondary",
  "Finished listing": "success",
  Available: "primary",
  Unavailable: "secondary",
  Resolved: "success",
};

const TrackedList = () => {
  const [popupData, setPopupData] = useState({});
  const [finishedListingPopup, setFinishedListingPopup] = useState(false);
  const [listOfTrackedMedicineItems, setListOfTrackedMedicineItems] = useState(
    []
  );

  const [selectedStatuses, setSelectedStatuses] = useState([
    "Listed",
    "Not listed",
    "Finished listing",
    "Expired",
  ]);
  const [errorMessage, setErrorMessage] = useState("");


  const openPopup = async ({ id, status }) => {
    try {
      const response = await getBuyingHospital(id);
      setPopupData(response.data);
      setFinishedListingPopup(true);
    } catch (error) {
      console.log("Error getting buying hospital");
    }
  };

  const filteredMedicines = useMemo(() => {
    return listOfTrackedMedicineItems.filter((medicineItem) =>
      selectedStatuses.includes(medicineItem.status)
    );
  }, [listOfTrackedMedicineItems, selectedStatuses]);


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


  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Medicine name", width: 200 },
    {
      field: "status",
      headerName: "Status",
      width: 150,
      renderCell: ({ row: { status, id, name } }) => (
        <ChipStatus status={status} openPopup={openPopup} id={id} name={name} />
      )
    },
    {
      field: "expired_date",
      headerName: "Tracking expired date",
      width: 250,
      renderCell: ({ row: { expired_date } }) => moment(expired_date).format("YYYY-MM-DD")
    },
  ]


  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(typeof value === "string" ? value.split(",") : value);
  };

  const getAllTrackedMedicineItems = async () => {
    try {
      const response = await getTrackingMedicines();
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
      await deleteTrackingMedicine(id);
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
    <div className={styles.contentContainer}>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <div className={styles.contentHeader}>
        <AddItemButton handleListChange={handleListChange} />
        <Filter
          statuses={["Listed", "Not listed", "Finished listing", "Expired"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className={styles.dataContainer}>
        {finishedListingPopup && (
          <FinishedListingPopup
            open={finishedListingPopup}
            onClose={setFinishedListingPopup}
            popupData={popupData}
          />
        )}

        <DataTable rows={filteredMedicines} columns={columns} handleDelete={handleDeleteMedicineItem} />
      </div>

    </div>
  );
};

TrackedList.propTypes = {};

export default TrackedList;
