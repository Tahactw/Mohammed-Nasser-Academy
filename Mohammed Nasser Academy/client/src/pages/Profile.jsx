import { useState, useEffect, useRef } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Avatar,
  Button,
  Tab,
  Tabs,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  CircularProgress,
  Rating,
} from '@mui/material';
import {
  Edit,
  Book,
  School,
  EmojiEvents,
  Comment,
  PhotoCamera,
  Close,
  AdminPanelSettings,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../lib/api';
import { supabase } from '../lib/supabase';
import { toast } from 'react-toastify';

function TabPanel({ children, value, index, ...other }) {
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const Profile = () => {
  const { user, profile, updateProfile, refreshProfile, isAdmin } = useAuth();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [tabValue, setTabValue] = useState(0);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editData, setEditData] = useState({
    full_name: '',
    bio: '',
    brief: '',
  });
  const [avatarLoading, setAvatarLoading] = useState(false);
  const [badges, setBadges] = useState([]);
  const [courses, setCourses] = useState([]);
  const [books, setBooks] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (profile) {
      fetchUserData();
      setEditData({
        full_name: profile.full_name || '',
        bio: profile.bio || '',
        brief: profile.brief || '',
      });
    }
  }, [profile]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const [badgesRes, coursesRes, booksRes, reviewsRes] = await Promise.all([
        api.get(`/api/users/${profile.id}/badges`),
        api.get(`/api/users/${profile.id}/courses`),
        api.get(`/api/users/${profile.id}/books`),
        api.get(`/api/users/${profile.id}/reviews`),
      ]);

      setBadges(badgesRes.data);
      setCourses(coursesRes.data);
      setBooks(booksRes.data);
      setReviews(reviewsRes.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setAvatarLoading(true);
    try {
      // Upload to Supabase Storage
      const fileExt = file.name.split('.').pop();
      const fileName = `${user.id}-${Date.now()}.${fileExt}`;
      const filePath = `avatars/${fileName}`;

      const { data, error } = await supabase.storage
        .from('avatars')
        .upload(filePath, file);

      if (error) throw error;

      // Get public URL
      const { data: { publicUrl } } = supabase.storage
        .from('avatars')
        .getPublicUrl(filePath);

      // Update profile
      await updateProfile({ avatar: publicUrl });
      toast.success('Profile picture updated!');
    } catch (error) {
      console.error('Error uploading avatar:', error);
      toast.error('Failed to update profile picture');
    } finally {
      setAvatarLoading(false);
    }
  };

  const handleEditSubmit = async () => {
    try {
      await updateProfile(editData);
      setEditDialogOpen(false);
      toast.success('Profile updated successfully!');
      await refreshProfile();
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  if (!profile) {
    return (
      <Container>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={4} textAlign="center">
              <Box position="relative" display="inline-block">
                <Avatar
                  src={profile.avatar}
                  sx={{ width: 150, height: 150, mb: 2 }}
                />
                {avatarLoading && (
                  <CircularProgress
                    size={150}
                    sx={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                    }}
                  />
                )}
                <input
                  type="file"
                  ref={fileInputRef}
                  hidden
                  accept="image/*"
                  onChange={handleAvatarChange}
                />
                <IconButton
                  color="primary"
                  sx={{
                    position: 'absolute',
                    bottom: 20,
                    right: -10,
                    bgcolor: 'background.paper',
                    boxShadow: 1,
                  }}
                  onClick={() => fileInputRef.current.click()}
                >
                  <PhotoCamera />
                </IconButton>
              </Box>
              <Typography variant="h4" gutterBottom>
                {profile.full_name}
              </Typography>
              {profile.brief && (
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  {profile.brief}
                </Typography>
              )}
              <Box mt={2}>
                <Button
                  variant="contained"
                  startIcon={<Edit />}
                  onClick={() => setEditDialogOpen(true)}
                  sx={{ mr: 2 }}
                >
                  Edit Profile
                </Button>
                {isAdmin() && (
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<AdminPanelSettings />}
                    onClick={() => navigate('/admin')}
                  >
                    Admin Panel
                  </Button>
                )}
              </Box>
            </Grid>
            <Grid item xs={12} md={8}>
              {profile.bio && (
                <Box mb={3}>
                  <Typography variant="h6" gutterBottom>
                    About
                  </Typography>
                  <Typography variant="body1">{profile.bio}</Typography>
                </Box>
              )}
              <Box display="flex" gap={2} flexWrap="wrap">
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h4" color="primary">
                      {courses.length}
                    </Typography>
                    <Typography variant="body2">Courses Enrolled</Typography>
                  </CardContent>
                </Card>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h4" color="primary">
                      {books.length}
                    </Typography>
                    <Typography variant="body2">Books Purchased</Typography>
                  </CardContent>
                </Card>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h4" color="primary">
                      {badges.length}
                    </Typography>
                    <Typography variant="body2">Badges Earned</Typography>
                  </CardContent>
                </Card>
              </Box>
            </Grid>
          </Grid>
        </Paper>

        <Paper elevation={3}>
          <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
            <Tab label="Badges" icon={<EmojiEvents />} />
            <Tab label="Courses" icon={<School />} />
            <Tab label="Books" icon={<Book />} />
            <Tab label="Reviews" icon={<Comment />} />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            {loading ? (
              <CircularProgress />
            ) : badges.length === 0 ? (
              <Typography>No badges earned yet</Typography>
            ) : (
              <Grid container spacing={2}>
                {badges.map((badge) => (
                  <Grid item xs={6} sm={4} md={3} key={badge.id}>
                    <Card>
                      <CardContent sx={{ textAlign: 'center' }}>
                        <Box fontSize={48}>{badge.icon}</Box>
                        <Typography variant="h6">{badge.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {badge.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            {loading ? (
              <CircularProgress />
            ) : courses.length === 0 ? (
              <Typography>No courses enrolled yet</Typography>
            ) : (
              <List>
                {courses.map((course) => (
                  <ListItem key={course.id} divider>
                    <ListItemText
                      primary={course.title}
                      secondary={
                        <Box>
                          <LinearProgress
                            variant="determinate"
                            value={course.progress || 0}
                            sx={{ mb: 1 }}
                          />
                          <Typography variant="caption">
                            Progress: {course.progress || 0}%
                          </Typography>
                        </Box>
                      }
                    />
                    <Chip
                      label={course.status}
                      color={
                        course.status === 'completed'
                          ? 'success'
                          : course.status === 'in_progress'
                          ? 'warning'
                          : 'default'
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {loading ? (
              <CircularProgress />
            ) : books.length === 0 ? (
              <Typography>No books purchased yet</Typography>
            ) : (
              <Grid container spacing={2}>
                {books.map((book) => (
                  <Grid item xs={12} sm={6} md={4} key={book.id}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6">{book.title}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {book.author}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            {loading ? (
              <CircularProgress />
            ) : reviews.length === 0 ? (
              <Typography>No reviews yet</Typography>
            ) : (
              <List>
                {reviews.map((review) => (
                  <ListItem key={review.id} divider>
                    <ListItemText
                      primary={review.course_id ? review.course_title : review.book_title}
                      secondary={
                        <Box>
                          <Rating value={review.rating} readOnly size="small" />
                          <Typography variant="body2">{review.comment}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {new Date(review.created_at).toLocaleDateString()}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </TabPanel>
        </Paper>

        {/* Edit Dialog */}
        <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>
            Edit Profile
            <IconButton
              onClick={() => setEditDialogOpen(false)}
              sx={{ position: 'absolute', right: 8, top: 8 }}
            >
              <Close />
            </IconButton>
          </DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Full Name"
              value={editData.full_name}
              onChange={(e) => setEditData({ ...editData, full_name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Brief (Short Description)"
              value={editData.brief}
              onChange={(e) => setEditData({ ...editData, brief: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Bio"
              value={editData.bio}
              onChange={(e) => setEditData({ ...editData, bio: e.target.value })}
              margin="normal"
              multiline
              rows={4}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleEditSubmit} variant="contained">
              Save Changes
            </Button>
          </DialogActions>
        </Dialog>
      </motion.div>
    </Container>
  );
};

export default Profile;
