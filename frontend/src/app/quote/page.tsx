'use client';

import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Container,
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

const quoteSchema = z.object({
  name: z.string().min(1, 'Name is required').min(2, 'Name must be at least 2 characters'),
  phone: z.string().min(1, 'Phone is required').regex(/^[\d\s\-\+\(\)]+$/, 'Invalid phone number'),
  address: z.string().min(1, 'Address is required').min(5, 'Address must be at least 5 characters'),
  serviceType: z.string().min(1, 'Service type is required'),
  description: z.string().optional(),
});

type QuoteFormData = z.infer<typeof quoteSchema>;

const serviceTypes = [
  'Plumbing',
  'Electrical',
  'HVAC',
  'Cleaning',
  'Landscaping',
  'Painting',
  'Carpentry',
  'Other',
];

export default function QuotePage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<QuoteFormData>({
    resolver: zodResolver(quoteSchema),
    defaultValues: {
      name: '',
      phone: '',
      address: '',
      serviceType: '',
      description: '',
    },
  });

  const onSubmit = async (data: QuoteFormData) => {
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const response = await fetch(`${API_BASE}/api/quotes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
{submitStatus && (
        <Alert severity={submitStatus.type} sx={{ mb: 3 }} onClose={() => setSubmitStatus(null)}>
          {submitStatus.message}
        </Alert>
      )}

      
      if (!response.ok) {
        throw new Error('Failed to submit quote request');
      }

      const result = await response.json();
      console.log('Quote submitted:', result);
      
      setSubmitStatus({
        type: 'success',
        message: 'Quote request submitted successfully! We will get back to you soon.',
      });
      reset();
    } catch (error) {
      console.error('Error submitting quote:', error);
      setSubmitStatus({
        type: 'error',
        message: 'Failed to submit quote request. Please try again.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Request a Quote
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Fill out the form below and we&apos;ll get back to you with a quote as soon as possible.
      </Typography>

      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
        }}
      >
        <Controller
          name="name"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Name"
              fullWidth
              required
              error={!!errors.name}
              helperText={errors.name?.message}
            />
          )}
        />

        <Controller
          name="phone"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Phone"
              fullWidth
              required
              error={!!errors.phone}
              helperText={errors.phone?.message}
              placeholder="+1 (555) 123-4567"
            />
          )}
        />

        <Controller
          name="address"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Address"
              fullWidth
              required
              multiline
              rows={2}
              error={!!errors.address}
              helperText={errors.address?.message}
            />
          )}
        />

        <Controller
          name="serviceType"
          control={control}
          render={({ field }) => (
            <FormControl fullWidth required error={!!errors.serviceType}>
              <InputLabel id="service-type-label">Service Type</InputLabel>
              <Select
                {...field}
                labelId="service-type-label"
                label="Service Type"
              >
                {serviceTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
              {errors.serviceType && (
                <FormHelperText>{errors.serviceType.message}</FormHelperText>
              )}
            </FormControl>
          )}
        />

        <Controller
          name="description"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Description (Optional)"
              fullWidth
              multiline
              rows={4}
              error={!!errors.description}
              helperText={errors.description?.message || 'Provide any additional details about your service request'}
              placeholder="Tell us more about what you need..."
            />
          )}
        />
          <Button
            type="reset"
            variant="outlined"
            size="large"
            disabled={isSubmitting}
            onClick={() => reset()}
          >
            Reset
          </Button>
          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={isSubmitting}
            startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : null}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Quote Request'}
          </Button>
        </Box>
    </Container>
  );
}
