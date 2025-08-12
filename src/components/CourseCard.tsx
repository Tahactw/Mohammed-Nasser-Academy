import React from 'react'
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  LinearProgress,
  Chip
} from '@mui/material'
import {
  Telegram,
  School,
  EmojiEvents,
  CalendarToday
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Course, CourseEnrollment } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { useAuth } from '@/context/AuthContext'

interface CourseCardProps {
  course: Course
  enrollment?: CourseEnrollment | null
}

const CourseCard: React.FC<CourseCardProps> = ({ course, enrollment: initialEnrollment }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const [enrollment, setEnrollment] = React.useState(initialEnrollment)

  React.useEffect(() => {
    const checkEnrollment = async () => {
      if (profile && !initialEnrollment) {
        const enrolled = await coursesApi.checkEnrollment(course.id, profile.id)
        setEnrollment(enrolled || null)
      }
    }
    checkEnrollment()
  }, [course.id, profile, initialEnrollment])

  const getStatusColor = () => {
    if (!enrollment) return 'default'
    switch (enrollment.status) {
      case 'completed':
        return 'success'
      case 'in_progress':
        return 'primary'
      default:
        return 'default'
    }
  }

  const getStatusText = () => {
    if (!enrollment) return t('enrollNow')
    switch (enrollment.status) {
      case 'completed':
        return t('completed')
      case 'in_progress':
        return t('inProgress')
      default:
        return t('notStarted')
    }
  }

  const handleEnrollClick = () => {
    window.open('https://t.me/your_admin_contact', '_blank')
  }

  const handleTelegramClick = () => {
    if (course.telegram_link) {
      window.open(course.telegram_link, '_blank')
    }
  }

  const handleCertificateDownload = () => {
    if (enrollment?.certificate_url) {
      window.open(enrollment.certificate_url, '_blank')
    }
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="200"
        image={course.image_url}
        alt={course.title}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="h2">
          {course.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {course.description}
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <CalendarToday sx={{ fontSize: 16, mr: 1 }} />
            <Typography variant="caption">
              {format(new Date(course.start_date), 'MMM dd, yyyy')} -{' '}
              {format(new Date(course.end_date), 'MMM dd, yyyy')}
            </Typography>
          </Box>

          {enrollment && (
            <>
              <Chip
                label={getStatusText()}
                color={getStatusColor() as any}
                size="small"
                sx={{ mb: 1 }}
              />
              <LinearProgress
                variant="determinate"
                value={enrollment.progress}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="text.secondary">
                {enrollment.progress}% {t('completed')}
              </Typography>
            </>
          )}
        </Box>
      </CardContent>

      <CardActions>
        {!enrollment ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<School />}
            onClick={handleEnrollClick}
          >
            {t('enrollNow')}
          </Button>
        ) : enrollment.status === 'completed' && enrollment.certificate_url ? (
          <Button
            fullWidth
            variant="contained"
            color="success"
            startIcon={<EmojiEvents />}
            onClick={handleCertificateDownload}
          >
            {t('downloadCertificate')}
          </Button>
        ) : course.telegram_link ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<Telegram />}
            onClick={handleTelegramClick}
          >
            {t('joinTelegram')}
          </Button>
        ) : null}
      </CardActions>
    </Card>
  )
}

export default CourseCard
