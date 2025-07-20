import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Skeleton,
} from '@mui/material';
import { ShoppingCart } from '@mui/icons-material';
import { motion } from 'framer-motion';
import api from '../lib/api';

const Books = () => {
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await api.get('/api/books');
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Typography variant="h2" component="h1" gutterBottom textAlign="center" sx={{ mb: 6 }}>
        My Books
      </Typography>

      <Grid container spacing={4}>
        {loading
          ? [...Array(6)].map((_, index) => (
              <Grid item key={index} xs={12} sm={6} md={4}>
                <Card>
                  <Skeleton variant="rectangular" height={300} />
                  <CardContent>
                    <Skeleton variant="text" sx={{ fontSize: '1.5rem' }} />
                    <Skeleton variant="text" />
                    <Skeleton variant="text" />
                  </CardContent>
                  <CardActions>
                    <Skeleton variant="rectangular" width={100} height={36} />
                  </CardActions>
                </Card>
              </Grid>
            ))
          : books.map((book, index) => (
              <Grid item key={book._id} xs={12} sm={6} md={4}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      transition: 'transform 0.3s ease',
                      '&:hover': {
                        transform: 'translateY(-5px)',
                        boxShadow: 6,
                      },
                    }}
                  >
                    <CardMedia
                      component="img"
                      height="300"
                      image={book.coverImage || '/placeholder-book.jpg'}
                      alt={book.title}
                      sx={{ objectFit: 'cover' }}
                    />
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Typography gutterBottom variant="h5" component="h2">
                        {book.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {book.shortDescription}
                      </Typography>
                      <Typography variant="h6" color="primary">
                        Pay What You Want (min ${book.minPrice || 10})
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button
                        size="large"
                        variant="contained"
                        startIcon={<ShoppingCart />}
                        onClick={() => navigate(`/books/${book._id}`)}
                        fullWidth
                      >
                        View Details
                      </Button>
                    </CardActions>
                  </Card>
                </motion.div>
              </Grid>
            ))}
      </Grid>
    </Container>
  );
};

export default Books;
