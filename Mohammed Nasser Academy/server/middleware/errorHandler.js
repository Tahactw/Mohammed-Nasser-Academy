const errorHandler = (err, req, res, next) => {
  console.error('Error:', err);

  // Supabase specific errors
  if (err.code === 'PGRST301') {
    return res.status(404).json({
      error: 'Resource not found',
      message: err.message
    });
  }

  if (err.code === '23505') {
    return res.status(409).json({
      error: 'Duplicate entry',
      message: 'This record already exists'
    });
  }

  // Default error
  res.status(err.status || 500).json({
    error: err.error || 'Internal server error',
    message: err.message || 'Something went wrong',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

const notFound = (req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: `Route ${req.originalUrl} not found`
  });
};

export default errorHandler;
export { notFound };
