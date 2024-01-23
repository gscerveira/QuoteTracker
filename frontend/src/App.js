import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import AuthForm from './components/AuthForm';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <Box
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
            bgcolor="background.default"
            p={2}
          >
            <Typography variant="h4" component="h1" gutterBottom>
              Quote Tracker
            </Typography>
            <AuthForm />
          </Box>
        } />
      </Routes>
    </Router>
  );
};

export default App;
