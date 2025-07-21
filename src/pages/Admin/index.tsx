import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import AdminLayout from './AdminLayout'
import Dashboard from './Dashboard'
import BooksManagement from './BooksManagement'
import CoursesManagement from './CoursesManagement'
import UsersManagement from './UsersManagement'
import TransactionsView from './TransactionsView'
import SiteSettings from './SiteSettings'

const AdminPage: React.FC = () => {
  const { profile } = useAuth()

  if (!profile?.is_admin) {
    return <Navigate to="/" replace />
  }

  return (
    <AdminLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/books" element={<BooksManagement />} />
        <Route path="/courses" element={<CoursesManagement />} />
        <Route path="/users" element={<UsersManagement />} />
        <Route path="/transactions" element={<TransactionsView />} />
        <Route path="/settings" element={<SiteSettings />} />
      </Routes>
    </AdminLayout>
  )
}

export default AdminPage