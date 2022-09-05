import React from "react";
import PropTypes from "prop-types";
import MedicineItem from "components/MedicineItem/MedicineItem";
const MedicineItems = ({ medicineItems }) => {
  return (
    <div>
      {medicineItems.map(({ medicineName, hospitalName, expirationDate }) => (
        <MedicineItem
          medicineName={medicineName}
          hospitalName={hospitalName}
          expirationDate={expirationDate}
        />
      ))}
    </div>
  );
};

MedicineItems.propTypes = {};

export default MedicineItems;
