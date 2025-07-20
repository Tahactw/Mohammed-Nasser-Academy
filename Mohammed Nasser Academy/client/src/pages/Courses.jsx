import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  CardMedia,
  Button,
  Stepper,
  Step,
  StepLabel,
  StepConnector,
  styled,
  stepConnectorClasses,
  Chip,
  Grid,
  LinearProgress,
  Avatar,
} from '@mui/material';
import {
  School,
  Lock,
  LockOpen,
  CheckCircle,
  RadioButtonUnchecked,
  Telegram,
  Timer,
  Person,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import api from '../lib/api';

const ColorlibConnector = styled(StepConnector)(({ theme }) => ({
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    top: 22,
  },
  [`&.${stepConnectorClasses.active}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      backgroundImage:
        'linear-gradient( 95deg,rgb(242,113,33) 0%,rgb(233,64,87) 50%,rgb(138,35,135) 100%)',
    },
  },
  [`&.${stepConnectorClasses.completed}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      backgroundImage:
        'linear-gradient( 95deg,rgb(242,113,33) 0%,rgb(233,64,87) 50%,rgb(138,35,135) 100%)',
    },
  },
  [`& .${stepConnectorClasses.line}`]: {
    height: 3,
    border: 0,
    backgroundColor:
      theme.palette.mode === 'dark' ? theme.palette.grey[800] : '#eaeaf0',
    borderRadius: 1,
  },
}));

const ColorlibStepIconRoot = styled('div')(({ theme, ownerState }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? theme.palette.grey[700] : '#ccc',
  zIndex: 1,
  color: '#fff',
  width: 50,
  height: 50,
  display: 'flex',
  borderRadius: '50%',
  justifyContent: 'center',
  alignItems: 'center',
  ...(ownerState.active && {
    backgroundImage:
      'linear-gradient( 136deg, rgb(242,113,33) 0%, rgb(233,64,87) 50%, rgb(138,35,135) 100%)',
    boxShadow: '0 4px 10px 0 rgba(0,0,0,.25)',
  }),
  ...(ownerState.completed && {
    backgroundImage:
      'linear-gradient( 136deg, rgb(242,113,33) 0%, rgb(233,64,87) 50%, rgb(138,35,135) 100%)',
  }),
}));

function ColorlibStepIcon(props) {
  const { active, completed, className } = props;

  return (
    <ColorlibStepIconRoot ownerState={{ completed, active }} className={className}>
      {completed ? <CheckCircle /> : <RadioButtonUnchecked />}
    </ColorlibStepIconRoot>
  );
}

const Courses = () => {
  const navigate = useNavigate();
  const { user, profile } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState({});

  useEffect(() => {
    fetchCourses();
  }, [user]);

  const fetchCourses = async () => {
    try {
      const response = await api.get('/api/courses');
      setCourses(response.data);
      
      if (user) {
        const progressRes = await api.get('/api/users/course-progress');
        const progressMap = {};
        progressRes.data.forEach(p => {
          progressMap[p.course_id] = p;
        });
        setProgress(progressMap);
      }
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActiveStep = () => {
    let lastCompleted = -1;
    courses.forEach((course, index) => {
      if (progress[course.id]?.status === 'completed') {
        lastCompleted = index;
      }
    });
    return Math.min(lastCompleted + 1, courses.length - 1);
  };

  const handleEnroll = async (courseId, telegramLink) => {
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      await api.post(`/api/courses/${courseId}/enroll`);
      window.open(telegramLink, '_blank');
      fetchCourses(); // Refresh to update progress
    } catch (error) {
      console.error('Error enrolling in course:', error);
    }
  };

  const canEnroll = (courseIndex) => {
    if (courseIndex === 0) return true;
    const previousCourse = courses[courseIndex - 1];
    return progress[previousCourse?.id]?.status === 'completed';
  };

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Typography variant="h2" component="h1" gutterBottom textAlign="center" sx={{ mb: 6 }}>
        Learning Path
      </Typography>

      {/* Timeline Progress */}
      <Box sx={{ mb: 8 }}>
        <Stepper
          alternativeLabel
          activeStep={getActiveStep()}
          connector={<ColorlibConnector />}
        >
          {courses.map((course, index) => (
            <Step key={course.id} completed={progress[course.id]?.status === 'completed'}>
              <StepLabel StepIconComponent={ColorlibStepIcon}>
                <Typography variant="caption">{course.title}</Typography>
              </StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>

      {/* Course Cards */}
      <Grid container spacing={4}>
        {courses.map((course, index) => {
          const courseProgress = progress[course.id];
          const isLocked = !canEnroll(index);
          const isEnrolled = !!courseProgress;
          const isCompleted = courseProgress?.status === 'completed';

          return (
            <Grid item xs={12} key={course.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card 
                  sx={{ 
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' },
                    opacity: isLocked ? 0.6 : 1,
                    position: 'relative',
                  }}
                >
                  {course.thumbnail && (
                    <CardMedia
                      component="img"
                      sx={{ 
                        width: { xs: '100%', md: 300 },
                        height: { xs: 200, md: 'auto' },
                      }}
                      image={course.thumbnail}
                      alt={course.title}
                    />
                  )}
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
                    <CardContent sx={{ flex: '1 0 auto' }}>
                      <Box display="flex" alignItems="center" mb={2}>
                        <Typography component="h5" variant="h5">
                          {course.title}
                        </Typography>
                        {isLocked && (
                          <Lock sx={{ ml: 2, color: 'text.secondary' }} />
                        )}
                        {isCompleted && (
                          <CheckCircle sx={{ ml: 2, color: 'success.main' }} />
                        )}
                      </Box>

                      <Typography variant="body1" color="text.secondary" paragraph>
                        {course.brief}
                      </Typography>

                      <Box display="flex" gap={2} mb={2}>
                        <Chip
                          icon={<School />}
                          label={course.difficulty_level || 'Intermediate'}
                          size="small"
                        />
                        <Chip
                          icon={<Person />}
                          label={`${course.enrolled_count || 0} enrolled`}
                          size="small"
                        />
                      </Box>

                      {isEnrolled && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="body2" gutterBottom>
                            Progress: {courseProgress.progress}%
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={courseProgress.progress} 
                            sx={{ height: 8, borderRadius: 4 }}
                          />
                        </Box>
                      )}
                    </CardContent>

                    <CardActions sx={{ p: 2 }}>
                      {isLocked ? (
                        <Button disabled startIcon={<Lock />}>
                          Complete Previous Course
                        </Button>
                      ) : isCompleted ? (
                        <Button
                          variant="outlined"
                          color="success"
                          startIcon={<CheckCircle />}
                          onClick={() => window.open(course.telegram_link, '_blank')}
                        >
                          Completed - Review on Telegram
                        </Button>
                      ) : isEnrolled ? (
                        <Button
                          variant="contained"
                          startIcon={<Telegram />}
                          onClick={() => window.open(course.telegram_link, '_blank')}
                        >
                          Continue on Telegram
                        </Button>
                      ) : (
                        <Button
                          variant="contained"
                          startIcon={<Telegram />}
                          onClick={() => handleEnroll(course.id, course.telegram_link)}
                        >
                          Start Course on Telegram
                        </Button>
                      )}
                    </CardActions>
                  </Box>
                </Card>
              </motion.div>
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
};

export default Courses;
