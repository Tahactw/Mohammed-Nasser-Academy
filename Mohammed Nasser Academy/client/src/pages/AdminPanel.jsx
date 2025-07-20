import { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Tabs,
  Tab,
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Chip,
  Grid,
  Card,
  CardContent,
  Alert,
  InputAdornment,
  Avatar,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  CheckCircle,
  Book,
  School,
  People,
  Dashboard as DashboardIcon,
  Upload,
  AttachMoney,
  EmojiEvents,
  Comment,
  Visibility,
  VisibilityOff,
  Telegram,
  ExitToApp,
} from '@mui/icons-material';
import { toast } from 'react-toastify';
import api from '../lib/api';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const AdminPanel = () => {
  const { profile, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalCourses: 0,
    totalBooks: 0,
    totalRevenue: 0,
  });

  // Users state
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [badgeDialog, setBadgeDialog] = useState(false);
  const [selectedBadge, setSelectedBadge] = useState('');
  const [badgeTemplates, setBadgeTemplates] = useState([]);
  const [customBadge, setCustomBadge] = useState({
    name: '',
    description: '',
    icon: '',
    color: '#FFD700',
  });

  // Courses state
  const [courses, setCourses] = useState([]);
  const [courseDialog, setCourseDialog] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  const [courseForm, setCourseForm] = useState({
    title: '',
    description: '',
    brief: '',
    telegram_link: '',
    difficulty_level: 'beginner',
    order_index: 0,
  });

  // Books state
  const [books, setBooks] = useState([]);
  const [bookDialog, setBookDialog] = useState(false);
  const [editingBook, setEditingBook] = useState(null);
  const [bookForm, setBookForm] = useState({
    title: '',
    author: '',
    description: '',
    brief: '',
    price: 0,
    category: '',
  });

  // Reviews state
  const [reviews, setReviews] = useState([]);
  const [reviewFilter, setReviewFilter] = useState('all');

  useEffect(() => {
    if (!isAdmin()) {
      navigate('/profile');
      return;
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersRes, coursesRes, booksRes, reviewsRes, badgesRes, statsRes] = await Promise.all([
        api.get('/api/admin/users'),
        api.get('/api/courses'),
        api.get('/api/books'),
        api.get('/api/admin/reviews'),
        api.get('/api/admin/badge-templates'),
        api.get('/api/admin/stats'),
      ]);

      setUsers(usersRes.data);
      setCourses(coursesRes.data);
      setBooks(booksRes.data);
      setReviews(reviewsRes.data);
      setBadgeTemplates(badgesRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching admin data:', error);
      toast.error('Failed to load admin data');
    }
  };

  // User Management Functions
  const handleDeleteUser = async (userId) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
      await api.delete(`/api/admin/users/${userId}`);
      toast.success('User deleted successfully');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete user');
    }
  };

  const handleAssignBadge = async () => {
    try {
      const badgeData = selectedBadge === 'custom' ? customBadge : badgeTemplates.find(b => b.id === selectedBadge);
      
      await api.post(`/api/admin/users/${selectedUser}/badges`, {
        name: badgeData.name,
        description: badgeData.description,
        icon: badgeData.icon,
        color: badgeData.color,
        badge_type: 'custom',
      });

      toast.success('Badge assigned successfully');
      setBadgeDialog(false);
      setSelectedUser(null);
      setSelectedBadge('');
      setCustomBadge({
        name: '',
        description: '',
        icon: '',
        color: '#FFD700',
      });
    } catch (error) {
      toast.error('Failed to assign badge');
    }
  };

  // Course Management Functions
  const handleSaveCourse = async () => {
    try {
      if (editingCourse) {
        await api.put(`/api/admin/courses/${editingCourse}`, courseForm);
        toast.success('Course updated successfully');
      } else {
        await api.post('/api/admin/courses', courseForm);
        toast.success('Course created successfully');
      }
      setCourseDialog(false);
      setEditingCourse(null);
      setCourseForm({
        title: '',
        description: '',
        brief: '',
        telegram_link: '',
        difficulty_level: 'beginner',
        order_index: 0,
      });
      fetchData();
    } catch (error) {
      toast.error('Failed to save course');
    }
  };

  const handleDeleteCourse = async (courseId) => {
    if (!confirm('Are you sure you want to delete this course?')) return;
    
    try {
      await api.delete(`/api/admin/courses/${courseId}`);
      toast.success('Course deleted successfully');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete course');
    }
  };

  // Book Management Functions
  const handleSaveBook = async () => {
    try {
      if (editingBook) {
        await api.put(`/api/admin/books/${editingBook}`, bookForm);
        toast.success('Book updated successfully');
      } else {
        await api.post('/api/admin/books', bookForm);
        toast.success('Book created successfully');
      }
      setBookDialog(false);
      setEditingBook(null);
      setBookForm({
        title: '',
        author: '',
        description: '',
        brief: '',
        price: 0,
        category: '',
      });
      fetchData();
    } catch (error) {
      toast.error('Failed to save book');
    }
  };

  const handleDeleteBook = async (bookId) => {
    if (!confirm('Are you sure you want to delete this book?')) return;
    
    try {
      await api.delete(`/api/admin/books/${bookId}`);
      toast.success('Book deleted successfully');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete book');
    }
  };

  // Review Management Functions
  const handleToggleReview = async (reviewId, isVisible) => {
    try {
      await api.patch(`/api/admin/reviews/${reviewId}`, { is_visible: !isVisible });
      toast.success('Review visibility updated');
      fetchData();
    } catch (error) {
      toast.error('Failed to update review');
    }
  };

  const handleDeleteReview = async (reviewId) => {
    if (!confirm('Are you sure you want to delete this review?')) return;
    
    try {
      await api.delete(`/api/admin/reviews/${reviewId}`);
      toast.success('Review deleted successfully');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete review');
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Admin Panel
        </Typography>
        <Button
          variant="outlined"
          startIcon={<ExitToApp />}
          onClick={() => navigate('/profile')}
        >
          Exit Admin Panel
        </Button>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Users
                  </Typography>
                  <Typography variant="h4">{stats.totalUsers}</Typography>
                </Box>
                <People color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Courses
                  </Typography>
                  <Typography variant="h4">{stats.totalCourses}</Typography>
                </Box>
                <School color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Books
                  </Typography>
                  <Typography variant="h4">{stats.totalBooks}</Typography>
                </Box>
                <Book color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Revenue
                  </Typography>
                  <Typography variant="h4">${stats.totalRevenue}</Typography>
                </Box>
                <AttachMoney color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={3}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Users" icon={<People />} />
          <Tab label="Courses" icon={<School />} />
          <Tab label="Books" icon={<Book />} />
          <Tab label="Reviews" icon={<Comment />} />
        </Tabs>

        {/* Users Tab */}
        <TabPanel value={tabValue} index={0}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Joined</TableCell>
                  <TableCell>Badges</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <Box display="flex" alignItems="center" gap={1}>
                        <Avatar src={user.avatar} sx={{ width: 32, height: 32 }}>
                          {user.full_name?.[0]}
                        </Avatar>
                        <Typography>{user.full_name}</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      {new Date(user.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>{user.badges?.length || 0}</TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        startIcon={<EmojiEvents />}
                        onClick={() => {
                          setSelectedUser(user.id);
                          setBadgeDialog(true);
                        }}
                      >
                        Add Badge
                      </Button>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Courses Tab */}
        <TabPanel value={tabValue} index={1}>
          <Box mb={2}>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => {
                setCourseForm({
                  title: '',
                  description: '',
                  brief: '',
                  telegram_link: '',
                  difficulty_level: 'beginner',
                  order_index: courses.length + 1,
                });
                setCourseDialog(true);
              }}
            >
              Add Course
            </Button>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Order</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Level</TableCell>
                  <TableCell>Enrolled</TableCell>
                  <TableCell>Telegram</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {courses.map((course) => (
                  <TableRow key={course.id}>
                    <TableCell>{course.order_index}</TableCell>
                    <TableCell>{course.title}</TableCell>
                    <TableCell>
                      <Chip 
                        label={course.difficulty_level} 
                        size="small"
                        color={
                          course.difficulty_level === 'beginner' ? 'success' :
                          course.difficulty_level === 'intermediate' ? 'warning' : 'error'
                        }
                      />
                    </TableCell>
                    <TableCell>{course.enrolled_count}</TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => window.open(course.telegram_link, '_blank')}
                      >
                        <Telegram />
                      </IconButton>
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => {
                          setEditingCourse(course.id);
                          setCourseForm({
                            title: course.title,
                            description: course.description,
                            brief: course.brief,
                            telegram_link: course.telegram_link,
                            difficulty_level: course.difficulty_level,
                            order_index: course.order_index,
                          });
                          setCourseDialog(true);
                        }}
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteCourse(course.id)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Books Tab */}
        <TabPanel value={tabValue} index={2}>
          <Box mb={2}>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => {
                setBookForm({
                  title: '',
                  author: '',
                  description: '',
                  brief: '',
                  price: 0,
                  category: '',
                });
                setBookDialog(true);
              }}
            >
              Add Book
            </Button>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Author</TableCell>
                  <TableCell>Price</TableCell>
                  <TableCell>Purchases</TableCell>
                  <TableCell>Rating</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {books.map((book) => (
                  <TableRow key={book.id}>
                    <TableCell>{book.title}</TableCell>
                    <TableCell>{book.author}</TableCell>
                    <TableCell>${book.price}</TableCell>
                    <TableCell>{book.purchase_count}</TableCell>
                    <TableCell>{book.rating || 'N/A'}</TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => {
                          setEditingBook(book.id);
                          setBookForm({
                            title: book.title,
                            author: book.author,
                            description: book.description,
                            brief: book.brief,
                            price: book.price,
                            category: book.category,
                          });
                          setBookDialog(true);
                        }}
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteBook(book.id)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Reviews Tab */}
        <TabPanel value={tabValue} index={3}>
          <Box mb={2}>
            <FormControl>
              <InputLabel>Filter</InputLabel>
              <Select
                value={reviewFilter}
                onChange={(e) => setReviewFilter(e.target.value)}
                size="small"
                sx={{ minWidth: 120 }}
              >
                <MenuItem value="all">All</MenuItem>
                <MenuItem value="visible">Visible</MenuItem>
                <MenuItem value="hidden">Hidden</MenuItem>
              </Select>
            </FormControl>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Item</TableCell>
                  <TableCell>Rating</TableCell>
                  <TableCell>Comment</TableCell>
                  <TableCell>Date</TableCell>
                  <TableCell>Visible</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {reviews
                  .filter(r => reviewFilter === 'all' || 
                    (reviewFilter === 'visible' && r.is_visible) ||
                    (reviewFilter === 'hidden' && !r.is_visible))
                  .map((review) => (
                  <TableRow key={review.id}>
                    <TableCell>{review.user_name}</TableCell>
                    <TableCell>
                      {review.course_id ? `Course: ${review.course_title}` : `Book: ${review.book_title}`}
                    </TableCell>
                    <TableCell>{review.rating}/5</TableCell>
                    <TableCell sx={{ maxWidth: 300 }}>
                      <Typography variant="body2" noWrap>
                        {review.comment}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {new Date(review.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => handleToggleReview(review.id, review.is_visible)}
                      >
                        {review.is_visible ? <Visibility /> : <VisibilityOff />}
                      </IconButton>
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteReview(review.id)}
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>
      </Paper>

      {/* Badge Assignment Dialog */}
      <Dialog open={badgeDialog} onClose={() => setBadgeDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Assign Badge</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Badge Template</InputLabel>
            <Select
              value={selectedBadge}
              onChange={(e) => setSelectedBadge(e.target.value)}
            >
              {badgeTemplates.map((template) => (
                <MenuItem key={template.id} value={template.id}>
                  {template.icon} {template.name}
                </MenuItem>
              ))}
              <MenuItem value="custom">Custom Badge</MenuItem>
            </Select>
          </FormControl>

          {selectedBadge === 'custom' && (
            <Box mt={2}>
              <TextField
                fullWidth
                label="Badge Name"
                value={customBadge.name}
                onChange={(e) => setCustomBadge({ ...customBadge, name: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Description"
                value={customBadge.description}
                onChange={(e) => setCustomBadge({ ...customBadge, description: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Icon (emoji)"
                value={customBadge.icon}
                onChange={(e) => setCustomBadge({ ...customBadge, icon: e.target.value })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Color"
                type="color"
                value={customBadge.color}
                onChange={(e) => setCustomBadge({ ...customBadge, color: e.target.value })}
                margin="normal"
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBadgeDialog(false)}>Cancel</Button>
          <Button onClick={handleAssignBadge} variant="contained">
            Assign Badge
          </Button>
        </DialogActions>
      </Dialog>

      {/* Course Dialog */}
      <Dialog open={courseDialog} onClose={() => setCourseDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingCourse ? 'Edit Course' : 'Add New Course'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={courseForm.title}
            onChange={(e) => setCourseForm({ ...courseForm, title: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Brief Description"
            value={courseForm.brief}
            onChange={(e) => setCourseForm({ ...courseForm, brief: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Full Description"
            value={courseForm.description}
            onChange={(e) => setCourseForm({ ...courseForm, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
          />
          <TextField
            fullWidth
            label="Telegram Link"
            value={courseForm.telegram_link}
            onChange={(e) => setCourseForm({ ...courseForm, telegram_link: e.target.value })}
            margin="normal"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Difficulty Level</InputLabel>
            <Select
              value={courseForm.difficulty_level}
              onChange={(e) => setCourseForm({ ...courseForm, difficulty_level: e.target.value })}
            >
              <MenuItem value="beginner">Beginner</MenuItem>
              <MenuItem value="intermediate">Intermediate</MenuItem>
              <MenuItem value="advanced">Advanced</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="Order Index"
            type="number"
            value={courseForm.order_index}
            onChange={(e) => setCourseForm({ ...courseForm, order_index: parseInt(e.target.value) })}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCourseDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveCourse} variant="contained">
            {editingCourse ? 'Update' : 'Create'} Course
          </Button>
        </DialogActions>
      </Dialog>

      {/* Book Dialog */}
      <Dialog open={bookDialog} onClose={() => setBookDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingBook ? 'Edit Book' : 'Add New Book'}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={bookForm.title}
            onChange={(e) => setBookForm({ ...bookForm, title: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Author"
            value={bookForm.author}
            onChange={(e) => setBookForm({ ...bookForm, author: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Brief Description"
            value={bookForm.brief}
            onChange={(e) => setBookForm({ ...bookForm, brief: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Full Description"
            value={bookForm.description}
            onChange={(e) => setBookForm({ ...bookForm, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
          />
          <TextField
            fullWidth
            label="Price"
            type="number"
            value={bookForm.price}
            onChange={(e) => setBookForm({ ...bookForm, price: parseFloat(e.target.value) })}
            margin="normal"
            InputProps={{
              startAdornment: <InputAdornment position="start">$</InputAdornment>,
            }}
          />
          <TextField
            fullWidth
            label="Category"
            value={bookForm.category}
            onChange={(e) => setBookForm({ ...bookForm, category: e.target.value })}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBookDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveBook} variant="contained">
            {editingBook ? 'Update' : 'Create'} Book
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminPanel;
