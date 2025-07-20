import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Card,
  CardContent,
  Chip,
  Alert,
  LinearProgress,
} from '@mui/material';
import {
  Telegram,
  School,
  Timer,
  Assignment,
  Lock,
  LockOpen,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import axios from 'axios';
import ReviewSection from '../components/common/ReviewSection';

const CourseDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, profile } = useAuth();
  
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [canAccess, setCanAccess] = useState(false);
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    fetchCourse();
  }, [id, profile]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/courses/${id}`);
      setCourse(response.data);
      
      // Check access and progress
      if (profile) {
        const courseProgress = profile.courseProgress?.[id];
        setProgress(courseProgress);
        
        // Check if user can access this course
        const courseIndex = response.data.order - 1;
        if (courseIndex === 0) {
          setCanAccess(true);
        } else {
          // Check if previous course is completed
          const allCourses = await axios.get(`${import.meta.env.VITE_API_URL}/api/courses`);
          const previousCourse = allCourses.data.find(c => c.order === courseIndex);
          if (previousCourse && profile.courseProgress?.[previousCourse._id]?.status === 'completed') {
            setCanAccess(true);
          }
        }
      }
    } catch (error) {
      console.error('Error fetching course:', error);
      toast.error('Failed to load course details');
    } finally {
      setLoading(false);
    }
  };

  const handleJoinCourse = async () => {
    if (!user) {
      toast.info('Please login to join courses');
      navigate('/login');
      return;
    }

    if (!canAccess) {
      toast.error('Please complete previous courses first');
      return;
    }

    try {
      // Update course progress to "in_progress"
      await axios.post(`${import.meta.env.VITE_API_URL}/api/courses/${id}/enroll`, {
        userId: user.id,
      });

      // Open Telegram link
      window.open(course.telegramLink, '_blank');
      
      toast.success('Course joined! Opening Telegram...');
      // Refresh to update progress
      fetchCourse();
    } catch (error) {
      toast.error('Failed to join course');
    }
  };

  if (loading) {
    return <Container sx={{ py: 8 }}>Loading...</Container>;
  }

  if (!course) {
    return <Container sx={{ py: 8 }}>Course not found</Container>;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          {course.title}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
          <Chip
            icon={<Timer />}
            label={`Duration: ${course.duration}`}
            color="primary"
          />
          <Chip
            icon={<Assignment />}
            label={`${course.lessonsCount} Lessons`}
            color="secondary"
          />
          {progress?.status && (
            <Chip
              label={progress.status === 'completed' ? 'Completed' : 'In Progress'}
              color={progress.status === 'completed' ? 'success' : 'warning'}
            />
          )}
        </Box>

        {!canAccess && (
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Lock sx={{ mr: 1 }} />
              This course is locked. Please complete the previous courses first.
            </Box>
          </Alert>
        )}
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              About This Course
            </Typography>
            <Typography variant="body1" paragraph>
              {course.description}
            </Typography>
            
            {course.syllabus && (
              <>
                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  Course Syllabus
                </Typography>
                <Stepper orientation="vertical">
                  {course.syllabus.map((lesson, index) => (
                    <Step key={index} active={true}>
                      <StepLabel>{lesson.title}</StepLabel>
                      <StepContent>
                        <Typography>{lesson.description}</Typography>
                      </StepContent>
                    </Step>
                  ))}
                </Stepper>
              </>
            )}
          </Paper>

          {/* Reviews Section */}
          <ReviewSection
            itemType="course"
            itemId={id}
            reviews={course.reviews || []}
            canReview={progress?.status === 'completed'}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <Box sx={{ position: 'sticky', top: 100 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Course Progress
                </Typography>
                
                {progress ? (
                  <Box sx={{ mb: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Progress</Typography>
                      <Typography variant="body2">{progress.progress}%</Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={progress.progress}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                ) : (
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Not enrolled yet
                  </Typography>
                )}

                {progress?.status === 'completed' ? (
                  <Box>
                    <Alert severity="success" sx={{ mb: 2 }}>
                      Congratulations! You've completed this course.
                    </Alert>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={<Telegram />}
                      href={course.telegramLink}
                      target="_blank"
                    >
                      Visit Telegram Group
                    </Button>
                  </Box>
                ) : (
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    startIcon={canAccess ? <Telegram /> : <Lock />}
                    onClick={handleJoinCourse}
                    disabled={!canAccess}
                  >
                    {canAccess ? 'Join Course on Telegram' : 'Course Locked'}
                  </Button>
                )}

                <Typography variant="caption" display="block" sx={{ mt: 2, textAlign: 'center' }}>
                  This course is conducted via Telegram
                </Typography>
              </CardContent>
            </Card>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default CourseDetail;
