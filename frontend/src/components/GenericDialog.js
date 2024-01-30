import React from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Select, MenuItem, InputLabel, FormControl
} from '@mui/material';
import { Form } from 'react-router-dom';

const GenericDialog = ({ open, handleClose, title, fields, handleSubmit, handleChange, selectOptions }) => {
    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                {fields.map((field, index) => {
                    if (field.type === 'select') {
                        return (
                            <FormControl fullWidth margin="dense" key={index}>
                                <InputLabel id={`${field.id}-label`}>{field.label}</InputLabel>
                                <Select
                                    labelId={`${field.id}-label`}
                                    id={field.id}
                                    name={field.name}
                                    value={field.value}
                                    label={field.label}
                                    onChange={handleChange}
                                >
                                    {selectOptions[field.name].map((option, optionIndex) => (
                                        <MenuItem key={optionIndex} value={option.value}>{option.label}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        );
                    } else {
                        return (
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
                        );
                    }
                })}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Cancel</Button>
                <Button onClick={handleSubmit}>Submit</Button>
            </DialogActions>
        </Dialog >
    );
};

export default GenericDialog;
