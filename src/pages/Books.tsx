import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  TextField,
  InputAdornment,
  Typography,
  CircularProgress,
  Paper
} from '@mui/material'
import { Search } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { booksApi } from '@/services/api/books'
import BookCard from '@/components/BookCard'

const BooksPage: React.FC = () => {
  const { t } = useTranslation()
  const [books, setBooks] = useState<Book[]>([])
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBooks()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = books.filter(
        book =>
          book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          book.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredBooks(filtered)
    } else {
      setFilteredBooks(books)
    }
  }, [searchQuery, books])

  const fetchBooks = async () => {
    try {
      const data = await booksApi.getAll()
      setBooks(data)
      setFilteredBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('books')}
      </Typography>

      <Paper sx={{ p: 2, mb: 4 }}>
        <TextField
          fullWidth
          placeholder={t('search')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Paper>

      <Grid container spacing={3}>
        {filteredBooks.map((book) => (
          <Grid item key={book.id} xs={12} sm={6} md={4} lg={3}>
            <BookCard book={book} />
          </Grid>
        ))}
      </Grid>

      {filteredBooks.length === 0 && (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            {searchQuery ? 'No books found matching your search.' : 'No books available.'}
          </Typography>
        </Box>
      )}
    </Box>
  )
}

export default BooksPage