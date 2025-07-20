import { Container, Typography, Box, Paper, Avatar } from '@mui/material';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <Container maxWidth="md" sx={{ py: 8 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Avatar
            src="/mohammed-nasser.jpg"
            alt="Mohammed Nasser"
            sx={{
              width: 200,
              height: 200,
              mx: 'auto',
              mb: 4,
              boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
            }}
          />
          
          <Typography variant="h2" component="h1" gutterBottom>
            Mohammed Nasser
          </Typography>
          
          <Typography variant="h5" color="text.secondary" paragraph>
            Writer, Instructor, and Digital Creator
          </Typography>
        </Box>

        <Paper elevation={0} sx={{ p: 4, backgroundColor: 'transparent' }}>
          <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', lineHeight: 1.8 }}>
            Welcome to my digital space. I'm Mohammed Nasser, a passionate writer and instructor dedicated to sharing knowledge and inspiring others through words and education.
          </Typography>
          
          <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', lineHeight: 1.8 }}>
            My journey began with a simple belief: that knowledge should be accessible to everyone. Through my books and courses, I strive to break down complex concepts into digestible, engaging content that empowers learners at all levels.
          </Typography>
          
          <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', lineHeight: 1.8 }}>
            Whether you're here to explore my written works or embark on a learning journey through my courses, I'm thrilled to have you as part of this community. Together, we'll explore new ideas, challenge conventional thinking, and grow both personally and professionally.
          </Typography>
          
          <Box sx={{ mt: 6, textAlign: 'center' }}>
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                repeatType: "reverse"
              }}
            >
              <Typography
                variant="h4"
                sx={{
                  background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  fontWeight: 700,
                }}
              >
                Let's Learn Together
              </Typography>
            </motion.div>
          </Box>
        </Paper>
      </motion.div>
    </Container>
  );
};

export default About;
