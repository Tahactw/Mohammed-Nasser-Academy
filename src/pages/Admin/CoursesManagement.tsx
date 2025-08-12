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
  Autocomplete,
  Chip
} from '@mui/material'
import { Edit, Delete, Add, People, Upload } from '@mui/icons-material'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { useTranslation } from 'react-i18next'
import { Course, CourseEnrollment, User } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { usersApi } from '@/services/api/users'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const CoursesManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [courses, setCourses] = useState<Course[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null)
  const [enrollments, setEnrollments] = useState<CourseEnrollment[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [enrollmentDialogOpen, setEnrollmentDialogOpen] = useState(false)
  const [editingCourse, setEditingCourse] = useState<Course | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    image_url: '',
    start_date: new Date().toISOString(),
    end_date: new Date().toISOString(),
    telegram_link: ''
  })
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [coursesData, usersData] = await Promise.all([
        coursesApi.getAll(),
        usersApi.getAllUsers()
      ])
      setCourses(coursesData)
      setUsers(usersData.filter(u => !u.is_banned))
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (course?: Course) => {
    if (course) {
      setEditingCourse(course)
      setFormData({
        title: course.title,
        description: course.description,
        image_url: course.image_url,
        start_date: course.start_date,
        end_date: course.end_date,
        telegram_link: course.telegram_link || ''
      })
    } else {
      setEditingCourse(null)
      setFormData({
        title: '',
        description: '',
        image_url: '',
        start_date: new Date().toISOString(),
        end_date: new Date().toISOString(),
        telegram_link: ''
      })
    }
    setDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    setEditingCourse(null)
    setImageFile(null)
  }

  const handleManageEnrollments = async (course: Course) => {
    setSelectedCourse(course)
    try {
      const enrollmentsData = await coursesApi.getCourseEnrollments(course.id)
      setEnrollments(enrollmentsData)
    } catch (error) {
      console.error('Error fetching enrollments:', error)
    }
    setEnrollmentDialogOpen(true)
  }

  const handleSave = async () => {
    try {
      let imageUrl = formData.image_url

      if (imageFile) {
        const path = `courses/${Date.now()}-${imageFile.name}`
        const { data, error } = await supabase.storage
          .from('course-images')
          .upload(path, imageFile, { upsert: true })
        
        if (error) throw error
        
        const { data: { publicUrl } } = supabase.storage
          .from('course-images')
          .getPublicUrl(path)
        
        imageUrl = publicUrl
      }

      const courseData = {
        ...formData,
        image_url: imageUrl
      }

      if (editingCourse) {
        await coursesApi.update(editingCourse.id, courseData)
        await adminApi.logAction(
          profile!.id,
          'update_course',
          'course',
          editingCourse.id,
          { title: courseData.title }
        )
      } else {
        const newCourse = await coursesApi.create(courseData)
        await adminApi.logAction(
          profile!.id,
          'create_course',
          'course',
          newCourse.id,
          { title: courseData.title }
        )
      }

      showNotification('Course saved successfully', 'success')
      handleCloseDialog()
      fetchData()
    } catch (error) {
      showNotification('Failed to save course', 'error')
    }
  }

  const handleDelete = async (course: Course) => {
    if (!window.confirm(`Are you sure you want to delete "${course.title}"?`)) {
      return
    }

    try {
      await coursesApi.delete(course.id)
      await adminApi.logAction(
        profile!.id,
        'delete_course',
        'course',
        course.id,
        { title: course.title }
      )
      showNotification('Course deleted successfully', 'success')
      fetchData()
    } catch (error) {
      showNotification('Failed to delete course', 'error')
    }
  }

  const handleEnrollUser = async () => {
    if (!selectedUser || !selectedCourse) return

    try {
      await coursesApi.enrollUser(selectedCourse.id, selectedUser.id)
      await adminApi.logAction(
        profile!.id,
        'enroll_user',
        'course_enrollment',
        selectedCourse.id,
        { 
          course: selectedCourse.title,
          user: selectedUser.username
        }
      )
      showNotification('User enrolled successfully', 'success')
      
      // Refresh enrollments
      const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
      setEnrollments(enrollmentsData)
      setSelectedUser(null)
    } catch (error) {
      showNotification('Failed to enroll user', 'error')
    }
  }

  const handleUpdateEnrollment = async (enrollment: CourseEnrollment, updates: Partial<CourseEnrollment>) => {
    try {
      await coursesApi.updateEnrollment(enrollment.id, updates)
      await adminApi.logAction(
        profile!.id,
        'update_enrollment',
        'course_enrollment',
        enrollment.id,
        updates
      )
      showNotification('Enrollment updated', 'success')
      
      // Refresh enrollments
      if (selectedCourse) {
        const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
        setEnrollments(enrollmentsData)
      }
    } catch (error) {
      showNotification('Failed to update enrollment', 'error')
    }
  }

  const handleRemoveEnrollment = async (enrollment: CourseEnrollment) => {
    if (!selectedCourse || !window.confirm('Remove this enrollment?')) return

    try {
      await coursesApi.removeEnrollment(selectedCourse.id, enrollment.user_id)
      await adminApi.logAction(
        profile!.id,
        'remove_enrollment',
        'course_enrollment',
        enrollment.id,
        { 
          course: selectedCourse.title,
          user: enrollment.user?.username
        }
      )
      showNotification('Enrollment removed', 'success')
      
      // Refresh enrollments
      const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
      setEnrollments(enrollmentsData)
    } catch (error) {
      showNotification('Failed to remove enrollment', 'error')
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('manageCourses')}</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Course
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Image</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Start Date</TableCell>
              <TableCell>End Date</TableCell>
              <TableCell>Enrollments</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {courses.map((course) => (
              <TableRow key={course.id}>
                <TableCell>
                  <img
                    src={course.image_url}
                    alt={course.title}
                    style={{ width: 60, height: 40, objectFit: 'cover' }}
                  />
                </TableCell>
                <TableCell>{course.title}</TableCell>
                <TableCell>
                  {new Date(course.start_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {new Date(course.end_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    startIcon={<People />}
                    onClick={() => handleManageEnrollments(course)}
                  >
                    Manage
                  </Button>
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpenDialog(course)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(course)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Course Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingCourse ? 'Edit Course' : 'Add Course'}</DialogTitle>
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
          
          <Box sx={{ mt: 2, mb: 2 }}>
            <DatePicker
              label="Start Date"
              value={new Date(formData.start_date)}
              onChange={(date) => date && setFormData({ ...formData, start_date: date.toISOString() })}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <DatePicker
              label="End Date"
              value={new Date(formData.end_date)}
              onChange={(date) => date && setFormData({ ...formData, end_date: date.toISOString() })}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </Box>

          <TextField
            fullWidth
            label="Telegram Group Link"
            value={formData.telegram_link}
            onChange={(e) => setFormData({ ...formData, telegram_link: e.target.value })}
            margin="normal"
          />
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Course Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setImageFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(imageFile || formData.image_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {imageFile ? imageFile.name : 'Current image uploaded'}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.title || !formData.description}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Enrollment Dialog */}
      <Dialog
        open={enrollmentDialogOpen}
        onClose={() => setEnrollmentDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Manage Enrollments - {selectedCourse?.title}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Autocomplete
                options={users.filter(u => !enrollments.some(e => e.user_id === u.id))}
                getOptionLabel={(option) => option.username}
                value={selectedUser}
                onChange={(_, value) => setSelectedUser(value)}
                renderInput={(params) => (
                  <TextField {...params} label="Select user to enroll" />
                )}
                sx={{ flex: 1 }}
              />
              <Button
                variant="contained"
                onClick={handleEnrollUser}
                disabled={!selectedUser}
              >
                Enroll
              </Button>
            </Box>
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Enrolled</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {enrollments.map((enrollment) => (
                  <TableRow key={enrollment.id}>
                    <TableCell>{enrollment.user?.username}</TableCell>
                    <TableCell>
                      <Chip
                        label={enrollment.status}
                        color={
                          enrollment.status === 'completed' ? 'success' :
                          enrollment.status === 'in_progress' ? 'primary' : 'default'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{enrollment.progress}%</TableCell>
                    <TableCell>
                      {new Date(enrollment.enrolled_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell align="right">
                      <Button
                        size="small"
                        onClick={() => handleUpdateEnrollment(enrollment, {
                          status: enrollment.status === 'completed' ? 'in_progress' : 'completed',
                          progress: enrollment.status === 'completed' ? 50 : 100,
                          completed_at: enrollment.status === 'completed' ? undefined : new Date().toISOString() // FIXED!
                        })}
                      >
                        Toggle Complete
                      </Button>
                      <IconButton
                        size="small"
                        onClick={() => handleRemoveEnrollment(enrollment)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEnrollmentDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default CoursesManagement