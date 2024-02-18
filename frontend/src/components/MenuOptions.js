import React from 'react';
import { IconButton, Menu, MenuItem } from '@mui/material';
import { MoreVertIcon } from '@mui/icons-material/MoreVert';

const MenuOptions = ({ onEdit, onDelete }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <IconButton
                aria-label="more"
                aria-controls="long-menu"
                aria-haspopup="true"
                onClick={handleClick}
            >
                <MoreVertIcon />
            </IconButton>
            <Menu
                id="long-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={() => { handleClose(); onEdit(); }}>Update</MenuItem>
                <MenuItem onClick={() => { handleClose(); onDelete(); }}>Delete</MenuItem>
            </Menu>
        </>
    );
};

export default MenuOptions;

