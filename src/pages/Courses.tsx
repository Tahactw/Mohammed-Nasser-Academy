import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Typography,
  CircularProgress
} from '@mui/material'
import { useTranslation } from 'react-i18next'
import { Course, CourseEnrollment } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { useAuth } from '@/context/AuthContext'
import CourseCard from '@/components/CourseCard'

const CoursesPage: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const [courses, setCourses] = useState<Course[]>([])
  const [enrollments, setEnrollments] = useState<CourseEnrollment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCourses()
  }, [profile])

  const fetchCourses = async () => {
    try {
      const coursesData = await coursesApi.getAll()
      setCourses(coursesData)

      if (profile) {
        const enrollmentsData = await coursesApi.getUserEnrollments(profile.id)
        setEnrollments(enrollmentsData)
      }
    } catch (error) {
      console.error('Error fetching courses:', error)
    } finally {
      setLoading(false)
    }
  }

  const getEnrollment = (courseId: string) => {
    return enrollments.find(e => e.course_id === courseId) || null
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
        {t('courses')}
      </Typography>

      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item key={course.id} xs={12} md={6} lg={4}>
            <CourseCard
              course={course}
              enrollment={getEnrollment(course.id)}
            />
          </Grid>
        ))}
      </Grid>

      {courses.length === 0 && (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            No courses available at the moment.
          </Typography>
        </Box>
      )}
    </Box>
  )
}

export default CoursesPage