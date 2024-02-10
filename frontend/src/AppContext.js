import React, { createContext, useState, useCallback } from 'react';
import { createProject, fetchProjects, fetchStores, createStore, fetchItems, createItem, updateItem } from './services/apiService';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
    const [projects, setProjects] = useState([]);
    const [currentProject, setCurrentProject] = useState(null);
    const [stores, setStores] = useState([]);
    const [items, setItems] = useState([]);
    // Other states will be added here as needed

    // Function to add a new project
    const addProject = (project) => {
        setProjects([...projects, project]);
        setCurrentProject(project);
    };

    const createAndAddProject = async (projectData) => {
        try {
            const newProject = await createProject(projectData);
            addProject(newProject);
        } catch (error) {
            console.error('Error creating project:', error);
            // Appropriate handling of error will be added here
        }
    };

    // Check if store exists, create it if it doesn't
    const findOrCreateStore = async (storeName) => {
        let store = stores.find(store => store.name === storeName);
        if (!store) {
            const newStore = await createStore({ name: storeName });
            setStores(prevStores => [...prevStores, newStore]);
            store = newStore; // Set store to the newly created store
        }
        return store; // Return either the existing store or the newly created store
    };

    const createAndAddItem = async (itemData, currentProjectId) => {
        try {
            const store = await findOrCreateStore(itemData.storeName);
            if (store && store.id) {
                const newItem = await createItem({ ...itemData, store: store.id, project: currentProjectId });
                setItems(prevItems => [...prevItems, newItem]);
            } else { 
                console.error('Error creating item');
                // Appropriate handling of error will be added here
            }
        } catch (error) {
            console.error('Error creating item:', error);
            // Appropriate handling of error will be added here
        };
    };

    const getProjects = useCallback(async () => {
        try {
            const fetchedProjects = await fetchProjects();
            setProjects(fetchedProjects);
        } catch (error) {
            console.error('Error fetching projects:', error);
            throw error;
        }
    }, []);

    const getStores = useCallback(async () => {
        try {
            const fetchedStores = await fetchStores();
            setStores(fetchedStores);
        } catch (error) {
            console.error('Error fetching stores:', error);
            throw error;
        }
    }, []);

    const addStore = async (storeData) => {
        try {
            const newStore = await createStore(storeData);
            setStores([...stores, newStore]);
        } catch (error) {
            console.error('Error creating store:', error);
            throw error;
        }
    };

    const getItems = async () => {
        try {
            const fetchedItems = await fetchItems();
            setItems(fetchedItems);
        } catch (error) {
            console.error('Error fetching items:', error);
            throw error;
        }
    };

    const addItem = async (itemData) => {
        try {
            const newItem = await createItem(itemData);
            setItems([...items, newItem]);
        } catch (error) {
            console.error('Error creating item:', error);
            throw error;
        }
    };

    const updateItemInContext = async (itemId, updatedItemData) => {
        try {
            const updatedItem = await updateItem(itemId, updatedItemData);
            setItems(prevItems => prevItems.map(item => item.id === itemId ? updatedItem : item));
        } catch (error) {
            console.error('Error updating item:', error);
            throw error;
        }
    };

    return (
        <AppContext.Provider value={{
            projects, stores, items, currentProject, addProject, createAndAddProject,
            getProjects, getStores, addStore, getItems, addItem, createAndAddItem, updateItemInContext
        }}>
            {children}
        </AppContext.Provider>
    );

};