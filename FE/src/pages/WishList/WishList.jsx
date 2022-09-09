import React, { useState, useEffect, useMemo } from "react";
import { Pagination, Alert } from "@mui/material";
import AddItemButton from "components/AddWishlistItemButton/AddWishlistItemButton";
import MedicineItems from "components/MedicineItems/MedicineItems";
import usePagination from "../../Utils/hooks/pagination";
import Filter from "components/Filter/Filter";
import "./WishList.css";
import { deleteSourceOrder, getSourceOrders } from "Utils/api/sourceOrder";
import ResolvedPopup from "components/WishListPopup/ResolvedPopup";

const WishList = () => {
  const [resolvedPopup, setResolvedPopup] = useState(false);
  const [availablePopup, setAvailablePopup] = useState(false);
  const [wishListItems, setWishListItems] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState([
    "Available",
    "Unavailable",
    "Resolved",
  ]);
  const [errorMessage, setErrorMessage] = useState("");

  const openPopup = ({ status }) => {
    if (status === "Unavailable") return setResolvedPopup(true);
    if (status === "Available") return setAvailablePopup(true);
  };

  const filteredWishListItems = useMemo(() => {
    return wishListItems.filter((wishListItem) =>
      selectedStatuses.includes(wishListItem.status)
    );
  }, [wishListItems, selectedStatuses]);

  const PER_PAGE = 7;
  const count = Math.ceil(filteredWishListItems.length / PER_PAGE);
  const filteredWishListToDisplay = usePagination(
    filteredWishListItems,
    PER_PAGE
  );

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

  const handlePageChange = (e, p) => {
    setCurrentPage(p);
    filteredWishListToDisplay.jump(p);
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
          statuses={["Available", "Unavailable", "Resolved"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className="data-container">
        {resolvedPopup && (
          <ResolvedPopup open={resolvedPopup} onClose={setResolvedPopup} />
        )}
        <MedicineItems
          medicineItems={filteredWishListToDisplay.currentData()}
          handleDelete={handleDeleteWishListItem}
          openPopup={openPopup}
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

WishList.propTypes = {};

export default WishList;
