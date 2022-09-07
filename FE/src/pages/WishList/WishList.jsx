import React, { useState, useEffect, useMemo } from "react";
import { Pagination, Alert } from "@mui/material";
import axios from "axios";
import AddItemButton from "components/AddWishlistItemButton/AddWishlistItemButton";
import MedicineItems from "components/MedicineItems/MedicineItems";
import usePagination from "../../Utils/hooks/pagination";
import Filter from "components/Filter/Filter";
import "./WishList.css";

const getWishListUrl = "http://localhost:8000/source-orders";
const deleteWishListUrl = "http://localhost:8000/source-order";

const WishList = () => {
  const [wishListItems, setWishListItems] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedStatuses, setSelectedStatuses] = useState([
    "AVAILABLE",
    "unavailable",
    "RESOLVED",
  ]);
  const [errorMessage, setErrorMessage] = useState("");

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
      console.log(
        "Error getting updated wishlist in handleListChange",
        error
      );
      setErrorMessage(error.detail.msg);
    }
  }

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
      await axios.delete(`${deleteWishListUrl}/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      await getAllWishListItems();
    } catch (error) {
      console.log("Error deleting item", error);
      setErrorMessage(error.detail.msg);
    }
  };

  const getAllWishListItems = async () => {
    try {
      const response = await axios.get(getWishListUrl, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
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
        <AddItemButton type="tracked list" handleListChange={handleListChange}/>
        <Pagination
          count={count}
          size="large"
          page={currentPage}
          variant="outlined"
          shape="rounded"
          onChange={handlePageChange}
        />
        <Filter
          statuses={["AVAILABLE", "unavailable", "RESOLVED"]}
          selectedStatuses={selectedStatuses}
          handleChange={handleFilterChange}
        />
      </div>
      <div className="data-container">
        <MedicineItems
          medicineItems={filteredWishListToDisplay.currentData()}
          handleDelete={handleDeleteWishListItem}
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
