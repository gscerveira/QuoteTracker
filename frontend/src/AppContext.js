import React, { createContext, useState } from 'react';
import { createProject } from './services/apiService';

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
        try{
            const newProject = await createProject(projectData);
            addProject(newProject);
        } catch (error) {
            console.error('Error creating project:', error);
            // Appropriate handling of error will be added here
        }
    };

    // Other functions will be added here as needed

    return (
        <AppContext.Provider value={{ projects, currentProject, addProject, createAndAddProject }}>
            {children}
        </AppContext.Provider>
    );

};