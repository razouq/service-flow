import type { Metadata } from 'next';
import { CssBaseline } from '@mui/material';
import { Box } from '@mui/material';
import Navbar from '@/components/Navbar';
import { ThemeProvider } from '@mui/material/styles';
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
          <CssBaseline />
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
