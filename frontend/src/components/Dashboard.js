import React, { useState, useEffect, useContext } from 'react';
import { Box, Drawer, List, ListItem, ListItemText, Button, Paper, Typography } from '@mui/material';
import { fetchProjects, createProject } from '../services/apiService';
import { reorder, move } from '../utils/dragAndDropHelpers';
import { AppContext } from '../AppContext';
import GenericDialog from './GenericDialog';
import KanbanBoard from './KanbanBoard';

const drawerWidth = 240;

const Dashboard = () => {
    const { projects, currentProject, createAndAddProject, createAndAddItem, updateItemInContext, getProjects, getStores, createStore, getItems, createItem, stores, items } = useContext(AppContext);

    const [selectedProject, setSelectedProject] = useState(null);

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

    const handleAddProject = () => {
        setDialogContext('project');
        setCurrentFormData({ name: '', description: '' });
        handleDialogOpen();
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

        await createAndAddProject(currentFormData);
        handleDialogClose();
    };

    const handleItemFormSubmit = async () => {
        if (!newItemFormData.name.trim() || !newItemFormData.description.trim() || !newItemFormData.storeName.trim()) {
            alert('Please fill in all the fields');
            return;
        }

        try {
            await createAndAddItem(newItemFormData, currentProject.id);
            handleItemDialogClose();
        } catch (error) {
            console.error('Error:', error);
            // Appropriate handling of error will be added here
        }


    };

    const handleDragEnd = async (result) => {
        const { destination, source, draggableId } = result;

        if (!destination) {
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

            const updatedItemData = { status: endStatus };
            try {
                const updatedItem = await updateItemInContext(draggableId, updatedItemData);
                console.log("Item updated successfully:", updatedItem);
            } catch (error) {
                console.error('Failed to update item:', error);
            }
        };
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
                        {projects.map((project) => (
                            <ListItem button key={project.id} onClick={() => handleProjectClick(project)}>
                                <ListItemText primary={project.name} />
                                <Button onClick={handleItemDialogOpen}>Add Item</Button>
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
                            <KanbanBoard items={items.filter(item => item.project === currentProject.id)} handleDragEnd={handleDragEnd} />
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
