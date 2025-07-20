import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { CircularProgress, Box, Typography } from '@mui/material';
import { useEffect, useState } from 'react';

const AdminRoute = ({ children }) => {
  const { user, profile, loading } = useAuth();
  const [checkingAdmin, setCheckingAdmin] = useState(true);

  useEffect(() => {
    // Give time for profile to load
    if (!loading && profile !== null) {
      setCheckingAdmin(false);
    } else if (!loading && !user) {
      setCheckingAdmin(false);
    }
  }, [loading, profile, user]);

  if (loading || checkingAdmin) {
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          Checking admin access...
        </Typography>
      </Box>
    );
  }

  if (!user) {
    console.log('AdminRoute: No user, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  if (!profile?.isAdmin) {
    console.log('AdminRoute: User is not admin, profile:', profile);
    return (
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography variant="h5" color="error">
          Access Denied
        </Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          You need admin privileges to access this page.
        </Typography>
      </Box>
    );
  }

  console.log('AdminRoute: User is admin, rendering admin panel');
  return children;
};

export default AdminRoute;
