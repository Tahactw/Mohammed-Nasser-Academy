import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress
} from '@mui/material'
import {
  People,
  MenuBook,
  School,
  AttachMoney
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { adminApi } from '@/services/api/admin'

interface StatCardProps {
  title: string
  value: number
  icon: React.ReactNode
  color: string
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => (
  <Paper sx={{ p: 3, height: '100%' }}>
    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
      <Box
        sx={{
          p: 1.5,
          borderRadius: 2,
          bgcolor: `${color}.100`,
          color: `${color}.main`,
          mr: 2
        }}
      >
        {icon}
      </Box>
      <Typography variant="h6">{title}</Typography>
    </Box>
    <Typography variant="h3" fontWeight="bold">
      {value.toLocaleString()}
    </Typography>
  </Paper>
)

const Dashboard: React.FC = () => {
  const { t } = useTranslation()
  const [stats, setStats] = useState({
    users: 0,
    books: 0,
    courses: 0,
    transactions: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await adminApi.getDashboardStats()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
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
        {t('dashboard')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Users"
            value={stats.users}
            icon={<People />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Books"
            value={stats.books}
            icon={<MenuBook />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Courses"
            value={stats.courses}
            icon={<School />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Transactions"
            value={stats.transactions}
            icon={<AttachMoney />}
            color="error"
          />
        </Grid>
      </Grid>

      {/* Add more dashboard widgets here */}
    </Box>
  )
}

export default Dashboard