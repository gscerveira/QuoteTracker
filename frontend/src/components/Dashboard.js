import React, { useState, useEffect } from 'react';
import { Box, Drawer, List, ListItem, ListItemText, Button, Paper, Typography } from '@mui/material';
import { fetchProjects, createProject } from '../services/apiService';

const drawerWidth = 240;

const Dashboard = () => {
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);

    useEffect(() => {
        // Fetch projects when component mounts
        const fetchAndSetProjects = async () => {
            const fetchedProjects = await fetchProjects();
            setProjects(fetchedProjects);
        };
        fetchAndSetProjects();
    }, []);

    const handleProjectClick = (project) => {
        setSelectedProject(project);
    };

    const handleAddProject = () => {
        // Implement functionality to add a new project
    };

    return (
        <Box sx={{ display: 'flex' }}>
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box',
                    },
                }}
                variant="permanent"
                anchor="left"
            >
                <List>
                    {projects.map((project, index) => (
                        <ListItem button key={project.id} onClick={() => handleProjectClick(project)}>
                            <ListItemText primary={project.name} />
                        </ListItem>
                    ))}
                </List>
                <Button onClick={handleAddProject}>+</Button>
            </Drawer>
            <Box
                component="main"
                sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
            >
                {selectedProject ? (
                    <Paper>
                        {/* Display selected project details here */}
                    </Paper>
                ) : (
                    <Typography variant="h6">Select a project to view details</Typography>
                )}
            </Box>
        </Box>
    );
};

export default Dashboard;
