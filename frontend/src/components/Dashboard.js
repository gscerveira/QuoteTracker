import React, { useState, useEffect, useContext } from 'react';
import { Box, Drawer, List, ListItem, ListItemText, Button, Paper, Typography, AppBar, Toolbar, Menu } from '@mui/material';
import MenuOptions from './MenuOptions';
import { reorder, move } from '../utils/dragAndDropHelpers';
import { AppContext } from '../AppContext';
import { useLogout } from '../utils/authHelpers';
import GenericDialog from './GenericDialog';
import KanbanBoard from './KanbanBoard';

const drawerWidth = 240;


const Dashboard = () => {
    const { projects, currentProject, setCurrentProject, createAndAddProject, createAndAddItem, updateItemInContext, deleteItemInContext, getProjects, getStores, createStore, getItems, getStore, createItem, stores, items, deleteProjectInContext, updateProjectInContext, findOrCreateStore } = useContext(AppContext);

    const handleLogout = useLogout();

    const [dialogOpen, setDialogOpen] = useState(false);
    const [itemDialogOpen, setItemDialogOpen] = useState(false);
    const [currentFormData, setCurrentFormData] = useState({ name: '', description: '' });
    const [newItemFormData, setNewItemFormData] = useState({ name: '', description: '', storeName: '' });
    const [dialogContext, setDialogContext] = useState(null); // ['project', 'item']
    const [columns, setColumns] = useState({
        need_to_send: [],
        sent: [],
        received: [],
        need_to_resend: [],
        done: [],
    });
    const [editingProjectId, setEditingProjectId] = useState(null);
    const [editingItemId, setEditingItemId] = useState(null);

    const handleAddProject = () => {
        setDialogContext('project');
        setCurrentFormData({ name: '', description: '' });
        handleDialogOpen();
    };

    const handleEditProject = (project) => {
        setDialogContext('project');
        setCurrentFormData({ name: project.name, description: project.description });
        setEditingProjectId(project.id);
        handleDialogOpen();
    };

    const handleEditItem = (item) => {
        setDialogContext('item');
        setNewItemFormData({ name: item.name, description: item.description, storeName: item.storeName });
        setEditingItemId(item.id);
        handleItemDialogOpen();
    };

    const handleDeleteItem = async (itemId) => {
        const isConfirmed = window.confirm('Are you sure you want to delete this item?');
        if (isConfirmed) {
            await deleteItemInContext(itemId);
        }
    };

    const handleDeleteProject = async (projectId) => {
        const isConfirmed = window.confirm('Are you sure you want to delete this project?');
        if (isConfirmed) {
            await deleteProjectInContext(projectId);

            if (currentProject && currentProject.id === projectId) {
                setCurrentProject(null);
            }
        }
    };

    const handleAddItem = () => {
        setDialogContext('item');
        setNewItemFormData({ name: '', description: '', storeName: '' });
        setItemDialogOpen(true);
    };

    const handleDialogOpen = () => setDialogOpen(true);
    const handleDialogClose = () => setDialogOpen(false);
    const handleItemDialogOpen = () => setItemDialogOpen(true);
    const handleItemDialogClose = () => setItemDialogOpen(false);

    const handleFormChange = (event) => {
        setCurrentFormData({ ...currentFormData, [event.target.name]: event.target.value });
    };

    const handleProjectFormSubmit = async () => {
        if (!currentFormData.name.trim() || !currentFormData.description.trim()) {
            alert('Please fill in all the fields');
            return;
        }

        if (editingProjectId) {
            await updateProjectInContext(editingProjectId, currentFormData);
        }
        else {
            await createAndAddProject(currentFormData);
        }

        handleDialogClose();
        setEditingProjectId(null);
    };

    const handleItemFormSubmit = async () => {
        if (!newItemFormData.name.trim() || !newItemFormData.description.trim() || !newItemFormData.storeName.trim()) {
            alert('Please fill in all the fields');
            return;
        }

        try {
            if (editingItemId) {
                await updateItemInContext(editingItemId, newItemFormData);
            }
            else {
                await createAndAddItem(newItemFormData, currentProject.id);
            }

            handleItemDialogClose();
            setEditingItemId(null);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleDragEnd = async (result) => {
        const { destination, source, draggableId } = result;

        if (!destination || (destination.droppableId === source.droppableId && destination.index === source.index)) {
            return;
        }

        const startStatus = source.droppableId;
        const endStatus = destination.droppableId;

        // If the item is dropped in the same column
        if (startStatus === endStatus) {
            const newItems = reorder(
                columns[startStatus],
                source.index,
                destination.index
            );
            updateColumnItems(startStatus, newItems);
        } else {
            // If the item is dropped in a different column
            const result = move(
                columns[startStatus],
                columns[endStatus],
                source,
                destination
            );
            updateColumnItems(startStatus, result[startStatus]);
            updateColumnItems(endStatus, result[endStatus]);
        }

        try {
            const updatedItemData = { status: endStatus };
            await updateItemInContext(draggableId, updatedItemData);
            console.log("Item updated successfully");
        } catch (error) {
            console.error('Failed to update item:', error);
        }
    };



    const updateColumnItems = (status, newItems) => {
        setColumns(prevColumns => ({
            ...prevColumns,
            [status]: newItems,
        }));
    };

    useEffect(() => {
        // Fetch projects when component mounts
        getProjects();
    }, [getProjects]);

    useEffect(() => {
        getStores();
    }, [getStores]);

    const handleProjectClick = (project) => {
        setCurrentProject(project);
    };

    return (
        <>
            <AppBar position="static" sx={{ mb: 2 }}>
                <Toolbar>
                    <Button
                        color="inherit"
                        sx={{ ml: 'auto' }}
                        onClick={handleLogout}
                    >
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>
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
                        {projects.map((project) => (
                            <ListItem
                                button
                                key={project.id}
                                onClick={() => handleProjectClick(project)}
                                secondaryAction={
                                    <MenuOptions
                                        onEdit={() => handleEditProject(project)}
                                        onDelete={() => handleDeleteProject(project.id)}
                                    />
                                }
                            >
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
                        <>
                            <Paper>
                                <Typography variant="h5">{currentProject.name}
                                    <Button
                                        onClick={handleAddItem}
                                        sx={{ marginLeft: 2 }}
                                    >
                                        +
                                    </Button>
                                </Typography>
                                <Typography variant="body1">{currentProject.description}</Typography>
                                {/* Add more project details or functionalities here */}
                            </Paper>
                            <KanbanBoard items={items.filter(item => item.project === currentProject.id)} handleDragEnd={handleDragEnd}
                                handleEditItem={handleEditItem} handleDeleteItem={handleDeleteItem} />
                        </>
                    ) : (
                        <Typography variant="h6" sx={{ textAlign: 'center' }}>Select a project to view details</Typography>
                    )}

                </Box>
            </Box>

            {dialogContext === 'project' && (
                <GenericDialog
                    open={dialogOpen}
                    handleClose={handleDialogClose}
                    title="Add New Project"
                    fields={[
                        { id: 'name', name: 'name', label: 'Name', type: 'text', value: currentFormData.name },
                        { id: 'description', name: 'description', label: 'Description', type: 'text', value: currentFormData.description }
                    ]}
                    handleSubmit={handleProjectFormSubmit}
                    handleChange={handleFormChange}
                />
            )}

            {itemDialogOpen && (
                <GenericDialog
                    open={itemDialogOpen}
                    handleClose={handleItemDialogClose}
                    title="Add New Item"
                    fields={[
                        { id: 'name', name: 'name', label: 'Name', type: 'text', value: newItemFormData.name },
                        { id: 'description', name: 'description', label: 'Description', type: 'text', value: newItemFormData.description },
                        { id: 'storeName', name: 'storeName', label: 'Store', type: 'autocomplete', value: newItemFormData.storeName }
                    ]}
                    autocompleteOptions={{
                        storeName: stores.map((store) => ({ label: store.name }))
                    }}
                    handleSubmit={handleItemFormSubmit}
                    handleChange={(e) => setNewItemFormData({ ...newItemFormData, [e.target.name]: e.target.value })}
                    selectOptions={{ storeName: stores.map((store) => ({ value: store.id, label: store.name })) }}
                />
            )}

        </>
    );
};


export default Dashboard;
