import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthForm from './components/AuthForm';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" >
          <Route path="/" element={<AuthForm />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
