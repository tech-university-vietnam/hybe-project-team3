import React from 'react'

import { DataGrid } from '@mui/x-data-grid';
import { IconButton } from "@mui/material";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";

const DataTable = ({ rows, columns, handleDelete }) => {

  // just to render MUI DataGrid
  const tableColumns = [
    ...columns,
    {
      field: "action",
      headerName: "Action",
      width: 250,

      // Important: passing id from customers state so I can delete or edit each user
      renderCell: ({ id }) => {
        return (
          <div style={{ width: '100%', height: '100%' }}>
            <IconButton
              onClick={() => {
                handleDelete(id);
              }}
              style={{ float: 'right' }}
            >
              <DeleteSweepIcon sx={{ color: "red" }} />
            </IconButton>
          </div>
        )
      }
    }
  ];

  return (
    <div style={{ height: '650px' }}>
      <DataGrid
        rows={rows}
        columns={tableColumns}
        pageSize={10}
        checkboxSelection={false}
      />
    </div>
  );
};

export default DataTable;