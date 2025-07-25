import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Avatar,
  Button,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Switch,
  FormControlLabel,
  TextField,
  CircularProgress,
  Divider,
  Badge as MuiBadge
} from '@mui/material'
import {
  Edit,
  Delete,
  Download,
  Message,
  Block,
  CardGiftcard,
  School,
  MenuBook,
  EmojiEvents,
  Settings,
  Notifications
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { User, BookOwnership, CourseEnrollment, UserBadge, Certificate, Message as MessageType } from '@/types'
import { usersApi } from '@/services/api/users'
import { messagesApi } from '@/services/api/messages'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { booksApi } from '@/services/api/books'
import { coursesApi } from '@/services/api/courses'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => {
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

const ProfilePage: React.FC = () => {
  const { userId } = useParams<{ userId?: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile: currentUser, updateProfile } = useAuth()
  const { showNotification } = useNotification()
  
  const [user, setUser] = useState<User | null>(null)
  const [tabValue, setTabValue] = useState(0)
  const [loading, setLoading] = useState(true)
  const [editingBio, setEditingBio] = useState(false)
  const [bio, setBio] = useState('')
  const [courseProgressPublic, setCourseProgressPublic] = useState(true)
  const [books, setBooks] = useState<BookOwnership[]>([])
  const [courses, setCourses] = useState<CourseEnrollment[]>([])
  const [badges, setBadges] = useState<UserBadge[]>([])
  const [certificates, setCertificates] = useState<Certificate[]>([])
  const [messages, setMessages] = useState<MessageType[]>([])
  const [giftHistory, setGiftHistory] = useState<BookOwnership[]>([])
  const [isBlocked, setIsBlocked] = useState(false)

  const isOwnProfile = !userId || userId === currentUser?.id
  const profileId = userId || currentUser?.id

  useEffect(() => {
    if (profileId) {
      fetchProfile()
      
      // Track profile visit
      if (!isOwnProfile && currentUser) {
        notificationsApi.notifyProfileVisit(profileId, currentUser.id, currentUser.username)
      }
    }
  }, [profileId])

  const fetchProfile = async () => {
    try {
      const userData = await usersApi.getProfile(profileId!)
      setUser(userData)
      setBio(userData.bio || '')
      setCourseProgressPublic(userData.course_progress_public)

      // Fetch related data
      const [
        booksData,
        coursesData,
        badgesData,
        certificatesData
      ] = await Promise.all([
        booksApi.getUserBooks(profileId!),
        coursesApi.getUserEnrollments(profileId!),
        usersApi.getUserBadges(profileId!),
        usersApi.getUserCertificates(profileId!)
      ])

      setBooks(booksData)
      setCourses(coursesData)
      setBadges(badgesData)
      setCertificates(certificatesData)

      // Fetch additional data for own profile
      if (isOwnProfile) {
        const messagesData = await messagesApi.getUserMessages(profileId!)
        setMessages(messagesData)
        
        // Filter gift history
        const giftsReceived = booksData.filter(b => b.is_gift)
        setGiftHistory(giftsReceived)
      }

      // Check if blocked
      if (currentUser && !isOwnProfile) {
        const blocked = await usersApi.isBlocked(currentUser.id, profileId!)
        setIsBlocked(blocked)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
      navigate('/404')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveBio = async () => {
    try {
      await updateProfile({ bio })
      setEditingBio(false)
      showNotification('Bio updated', 'success')
    } catch (error) {
      showNotification('Failed to update bio', 'error')
    }
  }

  const handleToggleCoursePrivacy = async () => {
    try {
      await updateProfile({ course_progress_public: !courseProgressPublic })
      setCourseProgressPublic(!courseProgressPublic)
      showNotification('Privacy settings updated', 'success')
    } catch (error) {
      showNotification('Failed to update privacy settings', 'error')
    }
  }

  const handleBlockUser = async () => {
    if (!currentUser || !user) return
    
    try {
      if (isBlocked) {
        await usersApi.unblockUser(currentUser.id, user.id)
        setIsBlocked(false)
        showNotification('User unblocked', 'success')
      } else {
        await usersApi.blockUser(currentUser.id, user.id)
        setIsBlocked(true)
        showNotification('User blocked', 'success')
      }
    } catch (error) {
      showNotification('Failed to update block status', 'error')
    }
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }

    try {
      await usersApi.deleteAccount(currentUser!.id)
      navigate('/')
    } catch (error) {
      showNotification('Failed to delete account', 'error')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  if (!user) {
    return null
  }

  return (
    <Box>
      {/* Profile Header */}
      <Paper sx={{ p: 4, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item>
            <Avatar
              src={user.avatar_url}
              sx={{ width: 120, height: 120 }}
            >
              {user.username[0].toUpperCase()}
            </Avatar>
          </Grid>
          <Grid item xs>
            <Typography variant="h4">{user.username}</Typography>
            {user.is_admin && (
              <Chip label="Admin" color="primary" size="small" sx={{ mt: 1 }} />
            )}
            
            {/* Badges */}
            <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
              {badges.map((userBadge) => (
                <MuiBadge
                  key={userBadge.id}
                  overlap="circular"
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  badgeContent={
                    <Avatar
                      src={userBadge.badge?.icon_url}
                      sx={{ width: 24, height: 24 }}
                    />
                  }
                >
                  <Chip
                    label={userBadge.badge?.name}
                    size="small"
                    variant="outlined"
                  />
                </MuiBadge>
              ))}
            </Box>

            {/* Bio */}
            <Box sx={{ mt: 2 }}>
              {editingBio && isOwnProfile ? (
                <Box>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Tell us about yourself..."
                    sx={{ mb: 1 }}
                  />
                  <Box>
                    <Button size="small" variant="contained" onClick={handleSaveBio}>
                      Save
                    </Button>
                    <Button
                      size="small"
                      onClick={() => {
                        setEditingBio(false)
                        setBio(user.bio || '')
                      }}
                      sx={{ ml: 1 }}
                    >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box>
                  <Typography variant="body1" color={user.bio ? 'inherit' : 'text.secondary'}>
                    {user.bio || 'No bio yet'}
                  </Typography>
                  {isOwnProfile && (
                    <IconButton size="small" onClick={() => setEditingBio(true)}>
                      <Edit />
                    </IconButton>
                  )}
                </Box>
              )}
            </Box>
          </Grid>
          {!isOwnProfile && currentUser && (
            <Grid item>
              <Button
                variant="contained"
                startIcon={<Message />}
                onClick={() => navigate(`/messages/${user.id}`)}
                disabled={isBlocked}
                sx={{ mb: 1 }}
              >
                Message
              </Button>
              <Button
                variant="outlined"
                startIcon={<Block />}
                onClick={handleBlockUser}
                color={isBlocked ? 'error' : 'inherit'}
                fullWidth
              >
                {isBlocked ? 'Unblock' : 'Block'}
              </Button>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="Books" icon={<MenuBook />} />
          <Tab label="Courses" icon={<School />} />
          {isOwnProfile && (
            <>
              <Tab label="Messages" icon={<Message />} />
              <Tab label="Gift History" icon={<CardGiftcard />} />
              <Tab label="Settings" icon={<Settings />} />
            </>
          )}
        </Tabs>
      </Paper>

      {/* Tab Panels */}
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>
          Book Ownership ({books.length})
        </Typography>
        <Grid container spacing={2}>
          {books.map((ownership) => (
            <Grid item xs={12} sm={6} md={4} key={ownership.id}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'start' }}>
                  <img
                    src={ownership.book?.cover_url}
                    alt={ownership.book?.title}
                    style={{ width: 60, height: 80, borderRadius: 4, marginRight: 16 }}
                  />
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle1">{ownership.book?.title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(ownership.purchase_date), 'MMM dd, yyyy')}
                    </Typography>
                    {ownership.is_gift && (
                      <Chip label="Gift" size="small" color="secondary" sx={{ ml: 1 }} />
                    )}
                    {isOwnProfile && (
                      <Box sx={{ mt: 1 }}>
                        <Button
                          size="small"
                          startIcon={<Download />}
                          onClick={() => window.open(ownership.book?.file_url, '_blank')}
                        >
                          Download
                        </Button>
                      </Box>
                    )}
                  </Box>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>
          Course History ({courses.length})
        </Typography>
        {(!isOwnProfile && !user.course_progress_public) ? (
          <Typography color="text.secondary">
            This user's course progress is private.
          </Typography>
        ) : (
          <List>
            {courses.map((enrollment) => (
              <ListItem key={enrollment.id}>
                <ListItemAvatar>
                  <Avatar src={enrollment.course?.image_url}>
                    <School />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={enrollment.course?.title}
                  secondary={
                    <>
                      Status: {enrollment.status} • Progress: {enrollment.progress}%
                      {enrollment.completed_at && (
                        <> • Completed: {format(new Date(enrollment.completed_at), 'MMM dd, yyyy')}</>
                      )}
                    </>
                  }
                />
                {enrollment.certificate_url && (
                  <ListItemSecondaryAction>
                    <IconButton
                      onClick={() => window.open(enrollment.certificate_url, '_blank')}
                    >
                      <EmojiEvents color="primary" />
                    </IconButton>
                  </ListItemSecondaryAction>
                )}
              </ListItem>
            ))}
          </List>
        )}
      </TabPanel>

      {isOwnProfile && (
        <>
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              Messages
            </Typography>
            <List>
              {messages.map((message) => (
                <ListItem key={message.id}>
                  <ListItemAvatar>
                    <Avatar src={
                      message.sender_id === currentUser?.id
                        ? message.recipient?.avatar_url
                        : message.sender?.avatar_url
                    }>
                      {(message.sender_id === currentUser?.id
                        ? message.recipient?.username[0]
                        : message.sender?.username[0]
                      )?.toUpperCase()}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      message.sender_id === currentUser?.id
                        ? `To: ${message.recipient?.username}`
                        : `From: ${message.sender?.username}`
                    }
                    secondary={
                      <>
                        {message.content.substring(0, 50)}...
                        <br />
                        {format(new Date(message.created_at), 'MMM dd, yyyy HH:mm')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              Gift History
            </Typography>
            <List>
              {giftHistory.map((gift) => (
                <ListItem key={gift.id}>
                  <ListItemAvatar>
                    <Avatar>
                      <CardGiftcard />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={gift.book?.title}
                    secondary={
                      <>
                        From: {gift.gifter?.username}
                        <br />
                        {gift.gift_message && `Message: ${gift.gift_message}`}
                        <br />
                        {format(new Date(gift.purchase_date), 'MMM dd, yyyy')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Typography variant="h6" gutterBottom>
              Settings
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Privacy
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={courseProgressPublic}
                    onChange={handleToggleCoursePrivacy}
                  />
                }
                label="Show course progress publicly"
              />
            </Box>

            <Divider sx={{ my: 3 }} />

            <Box>
              <Typography variant="subtitle1" gutterBottom color="error">
                Danger Zone
              </Typography>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={handleDeleteAccount}
              >
                Delete Account
              </Button>
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                This will permanently delete your account and all associated data.
              </Typography>
            </Box>
          </TabPanel>
        </>
      )}
    </Box>
  )
}

export default ProfilePage