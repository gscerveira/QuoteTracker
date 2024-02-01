import React from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Autocomplete, MenuItem, InputLabel, FormControl
} from '@mui/material';
import { Form } from 'react-router-dom';

const GenericDialog = ({ open, handleClose, title, fields, handleSubmit, handleChange, autocompleteOptions }) => {
    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                {fields.map((field, index) => {
                    if (field.type === 'autocomplete') {
                        return (
                            <Autocomplete
                                key={index}
                                freeSolo
                                autoSelect
                                options={autocompleteOptions['storeName'].map((option) => option.label)}
                                renderInput={(params) => (
                                    <TextField {...params} label="Store" margin="normal" variant="outlined" />
                                )}
                                onInputChange={(event, newInputValue) => {
                                    // Directly handle input changes to update form state
                                    handleChange({
                                        target: {
                                            name: 'storeName',
                                            value: newInputValue,
                                        },
                                    });
                                }}
                            />
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
