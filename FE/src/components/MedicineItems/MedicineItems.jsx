import React from "react";
import PropTypes from "prop-types";
import MedicineItem from "components/MedicineItem/MedicineItem";
const MedicineItems = ({ medicineItems }) => {
  return (
    <div>
      {medicineItems.map(
        ({ id, medicineName, hospitalName, expirationDate, status, handleDelete }) => (
          <MedicineItem
            key={id}
            medicineName={medicineName}
            hospitalName={hospitalName}
            expirationDate={expirationDate}
            status={status}
            handleDelete={handleDelete}
          />
        )
      )}
    </div>
  );
};

MedicineItems.propTypes = {
  medicineItems: PropTypes.arrayOf(
    PropTypes.shape({
      hospitalName: PropTypes.string,
      medicineName: PropTypes.string,
      expirationDate: PropTypes.string,
      status: PropTypes.string,
      handleDelete: PropTypes.func,
    })
  ),
};

export default MedicineItems;
