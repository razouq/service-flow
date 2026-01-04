'use client';

import {
  Alert,
  Box,
  Container,
  Typography,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

interface QuoteRow {
  id: string;
  name: string;
  phone: string;
  address: string;
  serviceType: string;
  description?: string;
  status?: string;
  createdAt?: string;
}

export default function QuotesPage() {
  const [rows, setRows] = useState<QuoteRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const columns = useMemo<GridColDef[]>(
    () => [
      { field: 'name', headerName: 'Name', flex: 1, minWidth: 150 },
      { field: 'phone', headerName: 'Phone', flex: 1, minWidth: 140 },
      { field: 'serviceType', headerName: 'Service Type', flex: 1, minWidth: 140 },
      {
        field: 'status',
        headerName: 'Status',
        flex: 1,
        minWidth: 120,
        valueGetter: (params) => params.value ?? 'SUBMITTED',
      },
      {
        field: 'createdAt',
        headerName: 'Created At',
        flex: 1,
        minWidth: 180,
        valueFormatter: (params) =>
          params.value ? new Date(params.value as string).toLocaleString() : '—',
      },
      { field: 'address', headerName: 'Address', flex: 2, minWidth: 200 },
      { field: 'description', headerName: 'Description', flex: 2, minWidth: 220 },
    ],
    []
  );

  useEffect(() => {
    const fetchQuotes = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE}/api/quotes`);
        if (!res.ok) {
          throw new Error('Failed to fetch quotes');
        }
        const data = await res.json();
        const quotes = Array.isArray(data?.quotes) ? data.quotes : [];
        const mapped: QuoteRow[] = quotes.map((q: any) => ({
          id: q._id ?? q.id,
          name: q.name,
          phone: q.phone,
          address: q.address,
          serviceType: q.serviceType,
          description: q.description,
          status: q.status,
          createdAt: q.createdAt,
        }));
        setRows(mapped);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchQuotes();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Quotes
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        Review all submitted quote requests.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 640, width: '100%' }}>
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(row) => row.id}
          loading={loading}
          disableRowSelectionOnClick
          initialState={{
            pagination: { paginationModel: { pageSize: 10, page: 0 } },
          }}
        />
      </Box>
    </Container>
  );
}
