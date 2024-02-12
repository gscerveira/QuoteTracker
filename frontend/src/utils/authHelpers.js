import { useNavigate } from 'react-router-dom';
import { logout } from '../services/apiService';

export const useLogout = () => {
    const history = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            history.push('/');
        } catch (error) {
            console.error('Error logging out:', error);
            // Appropriate handling of error will be added here
        }
    };

    return handleLogout;
};