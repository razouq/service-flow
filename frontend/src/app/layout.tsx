import type { Metadata } from 'next';
import { Box } from '@mui/material';
import Navbar from '@/components/Navbar';
import Providers from '@/providers';

export const metadata: Metadata = {
  title: 'ServiceFlow',
  description: 'Service operations management',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Navbar />

          <Box
            sx={{
              backgroundColor: '#f5f5f5',
              minHeight: '100vh',
            }}
          >
            {children}
          </Box>
        </Providers>
      </body>
    </html>
  );
}
