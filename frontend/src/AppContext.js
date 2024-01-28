import React, { createContext, useState, useCallback } from 'react';
import { createProject, fetchProjects } from './services/apiService';

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
    const [projects, setProjects] = useState([]);
    const [currentProject, setCurrentProject] = useState(null);
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

    const getProjects = useCallback(async () => {
        try {
            const fetchedProjects = await fetchProjects();
            setProjects(fetchedProjects);
        } catch (error) {
            console.error('Error fetching projects:', error);
            throw error;
        }
    }, []);

    return (
        <AppContext.Provider value={{ projects, currentProject, addProject, createAndAddProject, getProjects }}>
            {children}
        </AppContext.Provider>
    );

};