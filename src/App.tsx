import React, { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { CssBaseline, CircularProgress, Box } from '@mui/material'
import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import './i18n'

// Contexts
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { NotificationProvider } from './context/NotificationContext'
import { CartProvider } from './context/CartContext'
import { LanguageProvider } from './context/LanguageContext'

// Layout
import Layout from './components/Layout'

// Lazy load pages
const HomePage = lazy(() => import('./pages/Home'))
const BooksPage = lazy(() => import('./pages/Books'))
const BookDetailPage = lazy(() => import('./pages/BookDetail'))
const CoursesPage = lazy(() => import('./pages/Courses'))
const ProfilePage = lazy(() => import('./pages/Profile'))
const AdminPage = lazy(() => import('./pages/Admin'))
const RegisterPage = lazy(() => import('./pages/Register'))
const LoginPage = lazy(() => import('./pages/Login'))
const CartPage = lazy(() => import('./pages/Cart'))
const NotFoundPage = lazy(() => import('./pages/NotFound'))

// Loading component
const Loading = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
    <CircularProgress />
  </Box>
)

function App() {
  return (
    <BrowserRouter>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <LanguageProvider>
          <ThemeProvider>
            <AuthProvider>
              <NotificationProvider>
                <CartProvider>
                  <CssBaseline />
                  <Layout>
                    <Suspense fallback={<Loading />}>
                      <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/books" element={<BooksPage />} />
                        <Route path="/books/:id" element={<BookDetailPage />} />
                        <Route path="/courses" element={<CoursesPage />} />
                        <Route path="/profile/:userId?" element={<ProfilePage />} />
                        <Route path="/admin/*" element={<AdminPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/cart" element={<CartPage />} />
                        <Route path="/404" element={<NotFoundPage />} />
                        <Route path="*" element={<Navigate to="/404" replace />} />
                      </Routes>
                    </Suspense>
                  </Layout>
                </CartProvider>
              </NotificationProvider>
            </AuthProvider>
          </ThemeProvider>
        </LanguageProvider>
      </LocalizationProvider>
    </BrowserRouter>
  )
}

export default App