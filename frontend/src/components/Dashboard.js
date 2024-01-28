import React, { useState, useEffect, useContext } from 'react';
import { Box, Drawer, List, ListItem, ListItemText, Button, Paper, Typography } from '@mui/material';
import { fetchProjects, createProject } from '../services/apiService';
import { AppContext } from '../AppContext';
import GenericDialog from './GenericDialog';

const drawerWidth = 240;

const Dashboard = () => {
    const { projects, currentProject, createAndAddProject, getProjects } = useContext(AppContext);

    const [selectedProject, setSelectedProject] = useState(null);

    const [dialogOpen, setDialogOpen] = useState(false);
    const [currentFormData, setCurrentFormData] = useState({ name: '', description: '' });

    const handleAddProject = () => {
        setCurrentFormData({ name: '', description: '' });
        handleDialogOpen();
    };

    const handleDialogOpen = () => setDialogOpen(true);
    const handleDialogClose = () => setDialogOpen(false);

    const handleFormChange = (event) => {
        setCurrentFormData({ ...currentFormData, [event.target.name]: event.target.value });
    };

    const handleFormSubmit = async () => {
        if (!currentFormData.name.trim() || !currentFormData.description.trim()) {
            alert('Please fill in all the fields');
            return;
        }

        await createAndAddProject(currentFormData);
        handleDialogClose();
    };

    useEffect(() => {
        // Fetch projects when component mounts
        getProjects();
    }, [getProjects]);

    const handleProjectClick = (project) => {
        setSelectedProject(project);
    };

    return (
        <>
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
                    {currentProject ? (
                        <Paper>
                            <Typography variant="h5">{currentProject.name}</Typography>
                            <Typography variant="body1">{currentProject.description}</Typography>
                            {/* Add more project details or functionalities here */}
                        </Paper>
                    ) : (
                        <Typography variant="h6">Select a project to view details</Typography>
                    )}

                    {selectedProject ? (
                        <Paper>
                            {/* Display selected project details here */}
                        </Paper>
                    ) : (
                        <Typography variant="h6">Select a project to view details</Typography>
                    )}
                </Box>
            </Box>

            <GenericDialog
                open={dialogOpen}
                handleClose={handleDialogClose}
                title="Add New Project"
                fields={[
                    { id: 'name', name: 'name', label: 'Name', type: 'text', value: currentFormData.name },
                    { id: 'description', name: 'description', label: 'Description', type: 'text', value: currentFormData.description }
                ]}
                handleSubmit={handleFormSubmit}
                handleChange={handleFormChange}
            />

        </>
    );
};


export default Dashboard;
