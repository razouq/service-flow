'use client';

import QuotesTable from '@/components/QuotesTable';
import { fetchQuotes } from '@/features/quotes/client';
import { Quote } from '@/types/Quote';
import {
  Alert,
  Container,
  Typography,
} from '@mui/material';
import { useEffect, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export default function QuotesPage() {
  const [rows, setRows] = useState<Quote[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

 useEffect(() => {
  setLoading(true)
  setError(null)

  fetchQuotes()
    .then(setRows)
    .catch(err => setError(err.message ?? 'Unknown error'))
    .finally(() => setLoading(false))
}, [])

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
      <QuotesTable rows={rows} loading={loading} />
    </Container>
  );
}
