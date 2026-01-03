'use client';

import { AppBar, Toolbar, Typography, Button, Stack, Box } from '@mui/material';
import Link from 'next/link';
import LocalPhoneIcon from '@mui/icons-material/LocalPhone';

export default function Navbar() {
  return (
    <Box>
      <AppBar position="sticky" elevation={0} color="transparent">
        <Toolbar>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1 }}
          >
            ServiceFlow
          </Typography>

          <Stack direction="row" spacing={2}>
            <Button
              color="primary"
              component={Link}
              href="/quote"
              variant="contained"
              size='large'
              sx={{
                borderRadius: 8
              }}
            >
              Free Quote
            </Button>

            <Button
              variant="outlined"
              startIcon={<LocalPhoneIcon />}
              size='large'
              sx={{
                borderRadius: 8
              }}
            >
              +1 555 123 4567
            </Button>
          </Stack>
        </Toolbar>
        </AppBar>
      </Box>
  );
}
