import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Container, Typography, IconButton, Grow, Zoom } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { Book, School, Info, ExpandMore } from '@mui/icons-material';

const Home = () => {
  const navigate = useNavigate();
  const [expanded, setExpanded] = useState(false);

  const options = [
    { label: 'Books', icon: Book, path: '/books', color: '#ff6b6b' },
    { label: 'Courses', icon: School, path: '/courses', color: '#4ecdc4' },
    { label: 'About Me', icon: Info, path: '/about', color: '#ffe66d' },
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >

      
      {/* Animated background particles */}
      <Box
        sx={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          overflow: 'hidden',
        }}
      >
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            style={{
              position: 'absolute',
              width: Math.random() * 50 + 10,
              height: Math.random() * 50 + 10,
              borderRadius: '50%',
              background: 'rgba(255, 255, 255, 0.1)',
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              x: [0, Math.random() * 20 - 10, 0],
            }}
            transition={{
              duration: Math.random() * 5 + 5,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        ))}
      </Box>

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Typography
            variant="h1"
            sx={{
              color: 'white',
              fontWeight: 700,
              textAlign: 'center',
              mb: 2,
              fontSize: { xs: '3rem', md: '4rem' },
              textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
            }}
          >
            Mohammed Nasser
          </Typography>
          
          <Typography
            variant="h4"
            sx={{
              color: 'rgba(255, 255, 255, 0.9)',
              textAlign: 'center',
              mb: 6,
              fontSize: { xs: '1.5rem', md: '2rem' },
              fontWeight: 300,
            }}
          >
            Writer & Instructor
          </Typography>
        </motion.div>

        <Box sx={{ display: 'flex', justifyContent: 'center', position: 'relative', minHeight: 300 }}>
          <AnimatePresence>
            {!expanded ? (
              <motion.div
                key="button"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
                transition={{ duration: 0.3 }}
              >
                <IconButton
                  onClick={() => setExpanded(true)}
                  sx={{
                    width: 120,
                    height: 120,
                    background: 'rgba(255, 255, 255, 0.2)',
                    backdropFilter: 'blur(10px)',
                    border: '2px solid rgba(255, 255, 255, 0.3)',
                    color: 'white',
                    '&:hover': {
                      background: 'rgba(255, 255, 255, 0.3)',
                      transform: 'scale(1.1)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  <ExpandMore sx={{ fontSize: 60 }} />
                </IconButton>
              </motion.div>

              
            ) : (
              <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap', justifyContent: 'center' }}>
                {options.map((option, index) => (
                  <Grow
                    key={option.label}
                    in={expanded}
                    timeout={(index + 1) * 300}
                  >
                    <Box>
                      <motion.div
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <Box
                          onClick={() => navigate(option.path)}
                          sx={{
                            width: 180,
                            height: 180,
                            background: `linear-gradient(135deg, ${option.color} 0%, ${option.color}dd 100%)`,
                            borderRadius: 4,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            cursor: 'pointer',
                            boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
                            transition: 'all 0.3s ease',
                            '&:hover': {
                              boxShadow: '0 15px 40px rgba(0,0,0,0.4)',
                            },
                          }}
                        >
                          <option.icon sx={{ fontSize: 60, color: 'white', mb: 2 }} />
                          <Typography variant="h5" sx={{ color: 'white', fontWeight: 600 }}>
                            {option.label}
                          </Typography>
                        </Box>
                      </motion.div>
                    </Box>
                  </Grow>
                ))}
              </Box>
            )}
          </AnimatePresence>
        </Box>
      </Container>
    </Box>
  );
};

export default Home;
