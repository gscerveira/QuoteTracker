import React, { createContext, useState, useCallback } from 'react';
import { createProject, fetchProjects, fetchStores, createStore, fetchItems, createItem } from './services/apiService';

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

    const createAndAddItem = async (itemData, currentProjectId) => {
        try {
            // Check if store exists, create it if it doesn't
            const store = stores.find(store => store.name === itemData.storeName);
            if (!store) {
                const newStore = await createStore({ name: itemData.storeName });
                setStores(prevStores => [...prevStores, newStore]); // Add new store to stores state
            }

            // Create item
            const newItem = await createItem({ ...itemData, store: store.id, project: currentProjectId });
            setItems(prevItems => [...prevItems, newItem]); // Add new item to items state
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

    const getStores = async () => {
        try {
            const fetchedStores = await fetchStores();
            setStores(fetchedStores);
        } catch (error) {
            console.error('Error fetching stores:', error);
            throw error;
        }
    };

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

    return (
        <AppContext.Provider value={{
            projects, stores, items, currentProject, addProject, createAndAddProject,
            getProjects, getStores, addStore, getItems, addItem, createAndAddItem
        }}>
            {children}
        </AppContext.Provider>
    );

};