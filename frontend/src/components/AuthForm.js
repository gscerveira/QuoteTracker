import React, { useState } from 'react';
import { TextField, Button, Box, Tab, Tabs } from '@mui/material';
import { register, login } from '../services/apiService';
import { useNavigate } from 'react-router-dom';

const AuthForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });

    const navigate = useNavigate();

    const [isLogin, setIsLogin] = useState(true);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isLogin) {
                const response = await login(formData.username, formData.password);
                navigate('/dashboard')
            } else {
                const response = await register(formData.username, formData.email, formData.password);
                console.log(response.data);
            }
        }
        catch (error) {
            console.error(error.response.data);
        }
    };

    const handleTabChange = (e, newValue) => {
        setIsLogin(newValue === 0);
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Tabs value={isLogin ? 0 : 1} onChange={handleTabChange}>
            <Tab label="Login" />
            <Tab label="Register" />
          </Tabs>
          <TextField
            name="username"
            label="Username"
            value={formData.username}
            onChange={handleChange}
          />
          {!isLogin && (
            <TextField
              type="email"
              name="email"
              label="Email"
              value={formData.email}
              onChange={handleChange}
            />
          )}
          <TextField
            type="password"
            name="password"
            label="Password"
            value={formData.password}
            onChange={handleChange}
          />
          <Button type="submit" variant="contained">{isLogin ? 'Login' : 'Register'}</Button>
        </Box>
      );
    };


export default AuthForm;

