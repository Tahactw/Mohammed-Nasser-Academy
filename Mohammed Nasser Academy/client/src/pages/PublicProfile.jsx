import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Avatar,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
} from '@mui/material';
import { EmojiEvents, Book, School } from '@mui/icons-material';
import api from '../lib/api';

const PublicProfile = () => {
  const { userId } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      const response = await api.get(`/api/users/public/${userId}`);
      setProfile(response.data);
    } catch (error) {
      console.error('Error fetching public profile:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container sx={{ py: 8, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (!profile) {
    return (
      <Container sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h5">User not found</Typography>
      </Container>
    );
  }

  const completedCourses = Object.values(profile.courseProgress || {})
    .filter(c => c.status === 'completed').length;

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper sx={{ p: 4, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <Avatar
            src={profile.avatar}
            sx={{ width: 100, height: 100 }}
          >
            {profile.fullName?.charAt(0)}
          </Avatar>
          <Box>
            <Typography variant="h4" gutterBottom>
              {profile.fullName}
            </Typography>
            {profile.bio && (
              <Typography variant="body1" color="text.secondary">
                {profile.bio}
              </Typography>
            )}
          </Box>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <EmojiEvents sx={{ fontSize: 40, color: 'warning.main' }} />
              <Typography variant="h5">{profile.badges?.length || 0}</Typography>
              <Typography color="text.secondary">Badges Earned</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <School sx={{ fontSize: 40, color: 'success.main' }} />
              <Typography variant="h5">{completedCourses}</Typography>
              <Typography color="text.secondary">Courses Completed</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Book sx={{ fontSize: 40, color: 'primary.main' }} />
              <Typography variant="h5">{profile.reviews?.length || 0}</Typography>
              <Typography color="text.secondary">Reviews Written</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {profile.badges && profile.badges.length > 0 && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Badges
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {profile.badges.map((badge, index) => (
              <Chip
                key={index}
                label={badge.name}
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>
        </Paper>
      )}
    </Container>
  );
};

export default PublicProfile;
