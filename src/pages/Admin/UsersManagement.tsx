import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Avatar,
  TextField,
  InputAdornment,
  Menu,
  MenuItem,
  CircularProgress
} from '@mui/material'
import {
  Search,
  MoreVert,
  Block,
  Delete,
  AdminPanelSettings
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { User } from '@/types'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const UsersManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [users, setUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = users.filter(
        user =>
          user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredUsers(filtered)
    } else {
      setFilteredUsers(users)
    }
  }, [searchQuery, users])

  const fetchUsers = async () => {
    try {
      const data = await usersApi.getAllUsers()
      setUsers(data)
      setFilteredUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, user: User) => {
    setAnchorEl(event.currentTarget)
    setSelectedUser(user)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedUser(null)
  }

  const handleToggleBan = async () => {
    if (!selectedUser) return

    try {
      if (selectedUser.is_banned) {
        await usersApi.unbanUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'unban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User unbanned', 'success')
      } else {
        await usersApi.banUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'ban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User banned', 'success')
      }
      
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update ban status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleToggleAdmin = async () => {
    if (!selectedUser) return

    try {
      await usersApi.updateProfile(selectedUser.id, {
        is_admin: !selectedUser.is_admin
      })
      await adminApi.logAction(
        profile!.id,
        selectedUser.is_admin ? 'remove_admin' : 'make_admin',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification(
        selectedUser.is_admin ? 'Admin privileges removed' : 'Admin privileges granted',
        'success'
      )
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update admin status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleDeleteUser = async () => {
    if (!selectedUser || !window.confirm(`Delete user "${selectedUser.username}"? This cannot be undone.`)) {
      return
    }

    try {
      await usersApi.deleteAccount(selectedUser.id)
      await adminApi.logAction(
        profile!.id,
        'delete_user',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification('User deleted', 'success')
      fetchUsers()
    } catch (error) {
      showNotification('Failed to delete user', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleViewProfile = () => {
    if (selectedUser) {
      window.open(`/profile/${selectedUser.id}`, '_blank')
    }
    handleMenuClose()
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
        {t('manageUsers')}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search users..."
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

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Avatar</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Joined</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell>
                  <Avatar src={user.avatar_url} sx={{ width: 40, height: 40 }}>
                    {user.username[0].toUpperCase()}
                  </Avatar>
                </TableCell>
                <TableCell>
                  {user.username}
                  {user.is_admin && (
                    <Chip
                      icon={<AdminPanelSettings />}
                      label="Admin"
                      size="small"
                      color="primary"
                      sx={{ ml: 1 }}
                    />
                  )}
                </TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  {user.is_banned ? (
                    <Chip label="Banned" color="error" size="small" />
                  ) : user.email_verified ? (
                    <Chip label="Active" color="success" size="small" />
                  ) : (
                    <Chip label="Unverified" color="warning" size="small" />
                  )}
                </TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    onClick={(e) => handleMenuOpen(e, user)}
                    disabled={user.id === profile?.id}
                  >
                    <MoreVert />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewProfile}>
          View Profile
        </MenuItem>
        <MenuItem onClick={handleToggleBan}>
          <Block sx={{ mr: 1 }} />
          {selectedUser?.is_banned ? 'Unban User' : 'Ban User'}
        </MenuItem>
        <MenuItem onClick={handleToggleAdmin}>
          <AdminPanelSettings sx={{ mr: 1 }} />
          {selectedUser?.is_admin ? 'Remove Admin' : 'Make Admin'}
        </MenuItem>
        <MenuItem onClick={handleDeleteUser} sx={{ color: 'error.main' }}>
          <Delete sx={{ mr: 1 }} />
          Delete User
        </MenuItem>
      </Menu>
    </Box>
  )
}

export default UsersManagement
