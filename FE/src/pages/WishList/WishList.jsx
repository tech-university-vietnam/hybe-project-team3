import React, { useState, useEffect, useMemo } from "react";
import { Alert, Chip } from "@mui/material";
import AddItemButton from "components/AddWishlistItemButton/AddWishlistItemButton";
import Filter from "components/Filter/Filter";
import styles from "./WishList.module.css";
import DataTable from "components/DataTable/DataTable";

import { deleteSourceOrder, getSourceOrders } from "Utils/api/sourceOrder";
import AvailablePopup from "components/WishListPopup/AvailablePopup";
import ResolvedPopup from "components/WishListPopup/ResolvedPopup.jsx";
import { getSellingHospital } from "Utils/api/sourceOrder";
import moment from "moment/moment";


const badgeColorMap = {
  Listed: "primary",
  "Not listed": "secondary",
  "Finished listing": "success",
  Available: "primary",
  Unavailable: "secondary",
  Resolved: "success",
};

const WishList = () => {
  const [popupData, setPopupData] = useState();
  const [resolvedPopup, setResolvedPopup] = useState(false);
  const [availablePopup, setAvailablePopup] = useState(false);
  const [wishListItems, setWishListItems] = useState([]);
  const [selectedStatuses, setSelectedStatuses] = useState([
    "Available",
    "Unavailable",
    "Resolved",
  ]);
  const [errorMessage, setErrorMessage] = useState("");

  const openPopup = async ({ id, status, medicineName }) => {
    if (status === "Resolved") {
      try {
        const response = await getSellingHospital(id);
        setPopupData(response.data);
        setResolvedPopup(true);
      } catch (error) {
        console.log("error getting selling hospital", error);
      }
    } else if (status === "Available") {
      setAvailablePopup(true);
      setPopupData(medicineName);
    }
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Medicine name", width: 200 },
    {
      field: "status",
      headerName: "Status",
      width: 150,
      renderCell: ({ row: { status, id, name } }) => {
        return (
          <Chip
            onClick={
              ["Resolved", "Available", "Finished listing"].includes(status)
                ? () => openPopup({ id, status, name })
                : () => { }
            }
            label={status}
            color={badgeColorMap[status]}
            sx={{ fontWeight: "bold" }}
          />
        )
      }
    },
    {
      field: "expired_date",
      headerName: "Tracking expired date",
      width: 250,
      renderCell: ({ row: { expired_date } }) => moment(expired_date).format("YYYY-MM-DD")
    },
  ]

  const filteredWishListItems = useMemo(() => {
    return wishListItems.filter((wishListItem) =>
      selectedStatuses.includes(wishListItem.status)
    );
  }, [wishListItems, selectedStatuses]);


  const handleListChange = async () => {
    try {
      await getAllWishListItems();
    } catch (error) {
      console.log("Error getting updated wishlist in handleListChange", error);
      setErrorMessage(error.detail.msg);
    }
  };

  const handleFilterChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedStatuses(typeof value === "string" ? value.split(",") : value);
  };


  const handleDeleteWishListItem = async (id) => {
    try {
      await deleteSourceOrder(id);
      await getAllWishListItems();
    } catch (error) {
      console.log("Error deleting item", error);
      setErrorMessage(error.detail.msg);
    }
  };

  const getAllWishListItems = async () => {
    try {
      const response = await getSourceOrders();
      setWishListItems(response.data);
    } catch (error) {
      console.log(
        "Error getting list of wish list items in getAllWishListItems",
        error
      );
      setErrorMessage(error.detail.msg);
    }
  };

  useEffect(() => {
    getAllWishListItems();
  }, []);

  return (
    <div className={styles.contentContainer}>
      {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
      <div className={styles.contentHeader}>
        <AddItemButton
          type="tracked list"
          handleListChange={handleListChange}
        />
        <Filter
          statuses={["Available", "Unavailable", "Resolved"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className={styles.dataContainer}>
        {resolvedPopup && (
          <ResolvedPopup
            open={resolvedPopup}
            onClose={setResolvedPopup}
            popupData={popupData}
          />
        )}
        {availablePopup && (
          <AvailablePopup
            open={availablePopup}
            onClose={setAvailablePopup}
            name={popupData}
            resolve={handleListChange}
          />
        )}
        <DataTable rows={filteredWishListItems} columns={columns} handleDelete={handleDeleteWishListItem} />

      </div>
    </div>
  );
};

WishList.propTypes = {};

export default WishList;
