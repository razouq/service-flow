import { Quote } from "@/types/Quote";
import { Box } from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";

const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', flex: 1, minWidth: 150 },
    { field: 'phone', headerName: 'Phone', flex: 1, minWidth: 140 },
    { field: 'serviceType', headerName: 'Service Type', flex: 1, minWidth: 140 },
    {
      field: 'status',
      headerName: 'Status',
      flex: 1,
      minWidth: 120,
      valueGetter: (value) => value ?? 'SUBMITTED',
    },
    {
      field: 'createdAt',
      headerName: 'Created At',
      flex: 1,
      minWidth: 180,
      valueFormatter: (value) => 
        value ? new Date(value as string).toLocaleString() : '—',
    },
    { field: 'address', headerName: 'Address', flex: 2, minWidth: 200 },
    { field: 'description', headerName: 'Description', flex: 2, minWidth: 220 },
  ];

export default function QuotesTable({ rows, loading }: { rows: Quote[]; loading: boolean }) {
  return <Box sx={{ height: 640, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(row) => row.id}
          loading={loading}
          disableRowSelectionOnClick
          initialState={{
            pagination: { paginationModel: { pageSize: 10, page: 0 } },
          }}
          pageSizeOptions={[10, 25, 50]}
        />
      </Box>;
}