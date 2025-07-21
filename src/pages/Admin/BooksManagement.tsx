import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  InputAdornment
} from '@mui/material'
import { Edit, Delete, Add, Upload } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { booksApi } from '@/services/api/books'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const BooksManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingBook, setEditingBook] = useState<Book | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: 0,
    cover_url: '',
    file_url: ''
  })
  const [coverFile, setCoverFile] = useState<File | null>(null)
  const [bookFile, setBookFile] = useState<File | null>(null)

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      const data = await booksApi.getAll()
      setBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (book?: Book) => {
    if (book) {
      setEditingBook(book)
      setFormData({
        title: book.title,
        description: book.description,
        price: book.price,
        cover_url: book.cover_url,
        file_url: book.file_url
      })
    } else {
      setEditingBook(null)
      setFormData({
        title: '',
        description: '',
        price: 0,
        cover_url: '',
        file_url: ''
      })
    }
    setDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    setEditingBook(null)
    setCoverFile(null)
    setBookFile(null)
  }

  const handleUploadFile = async (file: File, bucket: string, path: string) => {
    try {
      const { data, error } = await supabase.storage
        .from(bucket)
        .upload(path, file, { upsert: true })
      
      if (error) throw error
      
      const { data: { publicUrl } } = supabase.storage
        .from(bucket)
        .getPublicUrl(path)
      
      return publicUrl
    } catch (error) {
      console.error('Upload error:', error)
      throw error
    }
  }

  const handleSave = async () => {
    try {
      let coverUrl = formData.cover_url
      let fileUrl = formData.file_url

      // Upload cover if new file selected
      if (coverFile) {
        const path = `covers/${Date.now()}-${coverFile.name}`
        coverUrl = await handleUploadFile(coverFile, 'book-covers', path)
      }

      // Upload book file if new file selected
      if (bookFile) {
        const path = `books/${Date.now()}-${bookFile.name}`
        fileUrl = await handleUploadFile(bookFile, 'book-files', path)
      }

      const bookData = {
        ...formData,
        cover_url: coverUrl,
        file_url: fileUrl
      }

      if (editingBook) {
        await booksApi.update(editingBook.id, bookData)
        await adminApi.logAction(
          profile!.id,
          'update_book',
          'book',
          editingBook.id,
          { title: bookData.title }
        )
      } else {
        const newBook = await booksApi.create(bookData)
        await adminApi.logAction(
          profile!.id,
          'create_book',
          'book',
          newBook.id,
          { title: bookData.title }
        )
      }

      showNotification('Book saved successfully', 'success')
      handleCloseDialog()
      fetchBooks()
    } catch (error) {
      showNotification('Failed to save book', 'error')
    }
  }

  const handleDelete = async (book: Book) => {
    if (!window.confirm(`Are you sure you want to delete "${book.title}"?`)) {
      return
    }

    try {
      await booksApi.delete(book.id)
      await adminApi.logAction(
        profile!.id,
        'delete_book',
        'book',
        book.id,
        { title: book.title }
      )
      showNotification('Book deleted successfully', 'success')
      fetchBooks()
    } catch (error) {
      showNotification('Failed to delete book', 'error')
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('manageBooks')}</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Book
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Cover</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books.map((book) => (
              <TableRow key={book.id}>
                <TableCell>
                  <img
                    src={book.cover_url}
                    alt={book.title}
                    style={{ width: 50, height: 70, objectFit: 'cover' }}
                  />
                </TableCell>
                <TableCell>{book.title}</TableCell>
                <TableCell>${book.price}</TableCell>
                <TableCell>
                  {new Date(book.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpenDialog(book)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(book)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingBook ? 'Edit Book' : 'Add Book'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
            required
          />
          <TextField
            fullWidth
            label="Price"
            type="number"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: Number(e.target.value) })}
            margin="normal"
            InputProps={{
              startAdornment: <InputAdornment position="start">$</InputAdornment>,
            }}
            required
          />
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Cover Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setCoverFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(coverFile || formData.cover_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {coverFile ? coverFile.name : 'Current cover uploaded'}
              </Typography>
            )}
          </Box>

          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Book File (PDF)
              <input
                type="file"
                hidden
                accept=".pdf"
                onChange={(e) => setBookFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(bookFile || formData.file_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {bookFile ? bookFile.name : 'Current file uploaded'}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.title || !formData.description || formData.price <= 0}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default BooksManagement