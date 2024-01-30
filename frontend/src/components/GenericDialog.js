import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
Select, MenuItem, InputLabel, FormControl } from '@mui/material';

const GenericDialog = ({ open, handleClose, title, fields, handleSubmit, handleChange }) => {
    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                {fields.map((field, index) => (
                    <TextField
                        key={index}
                        margin="dense"
                        id={field.id}
                        label={field.label}
                        type={field.type}
                        fullWidth
                        variant="standard"
                        name={field.name}
                        value={field.value}
                        onChange={handleChange}
                    />
                ))}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Cancel</Button>
                <Button onClick={handleSubmit}>Submit</Button>
            </DialogActions>
        </Dialog>
    );
};

export default GenericDialog;
