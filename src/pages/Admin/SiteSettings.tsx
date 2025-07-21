import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider
} from '@mui/material'
import { Save } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { adminApi } from '@/services/api/admin'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

const SiteSettings: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [settings, setSettings] = useState({
    site_name: 'React Academy',
    site_description: 'Your journey to knowledge starts here',
    maintenance_mode: false,
    registration_enabled: true,
    email_verification_required: true,
    max_file_size_mb: 50,
    allowed_file_types: ['pdf'],
    telegram_admin_contact: '',
    support_email: ''
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const data = await adminApi.getSiteSettings()
      if (data) {
        setSettings(prev => ({ ...prev, ...data }))
      }
    } catch (error) {
      console.error('Error fetching settings:', error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      await adminApi.updateSiteSettings(settings)
      await adminApi.logAction(
        profile!.id,
        'update_settings',
        'site_settings',
        'global',
        settings
      )
      showNotification('Settings saved successfully', 'success')
    } catch (error) {
      showNotification('Failed to save settings', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('siteSettings')}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          General Settings
        </Typography>
        
        <TextField
          fullWidth
          label="Site Name"
          value={settings.site_name}
          onChange={(e) => setSettings({ ...settings, site_name: e.target.value })}
          margin="normal"
        />

        <TextField
          fullWidth
          label="Site Description"
          value={settings.site_description}
          onChange={(e) => setSettings({ ...settings, site_description: e.target.value })}
          margin="normal"
          multiline
          rows={2}
        />

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          System Settings
        </Typography>

        <FormControlLabel
          control={
            <Switch
              checked={settings.maintenance_mode}
              onChange={(e) => setSettings({ ...settings, maintenance_mode: e.target.checked })}
            />
          }
          label="Maintenance Mode"
          sx={{ display: 'block', mb: 2 }}
        />

        <FormControlLabel
          control={
            <Switch
              checked={settings.registration_enabled}
              onChange={(e) => setSettings({ ...settings, registration_enabled: e.target.checked })}
            />
          }
          label="Registration Enabled"
          sx={{ display: 'block', mb: 2 }}
        />

        <FormControlLabel
          control={
            <Switch
              checked={settings.email_verification_required}
              onChange={(e) => setSettings({ ...settings, email_verification_required: e.target.checked })}
            />
          }
          label="Email Verification Required"
          sx={{ display: 'block', mb: 2 }}
        />

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Contact Settings
        </Typography>

        <TextField
          fullWidth
          label="Telegram Admin Contact"
          value={settings.telegram_admin_contact}
          onChange={(e) => setSettings({ ...settings, telegram_admin_contact: e.target.value })}
          margin="normal"
          placeholder="https://t.me/your_admin"
        />

        <TextField
          fullWidth
          label="Support Email"
          type="email"
          value={settings.support_email}
          onChange={(e) => setSettings({ ...settings, support_email: e.target.value })}
          margin="normal"
        />

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={handleSave}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Settings'}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}

export default SiteSettings