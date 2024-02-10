import React from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { Grid, Typography, Paper, Card, CardContent } from '@mui/material';

// Item organization helper function
const organizeItemByStatus = (items) => {
    const columns = {
        needToSend: [],
        sent: [],
        received: [],
        needToResend: [],
        done: [],
    };

    items.forEach((item) => {
        if (columns[item.status]) {
            columns[item.status].push(item);
        }
    });

    return columns;
};

const KanbanBoard = ({ items, onDragEnd }) => {
    const columns = organizeItemByStatus(items);

    return (
        <DragDropContext onDragEnd={handleDragEnd}>
            <Grid container spacing={2}>
                {Object.entries(columns).map(([status, items], index) => (
                    <Droppable droppableId={status} key={status}>
                        {(provided) => (
                            <Grid item xs={12} sm={6} md={4} lg={2.4}>
                                <Paper ref={provided.innerRef} {...provided.droppableProps} style={{ minHeight: 500 }}>
                                    <Typography variant="h6" style={{ padding: '16px 0', textAlign: 'center' }}>
                                        {status.replace('_', ' ')}
                                    </Typography>
                                    {items.map((item, index) => (
                                        <Draggable key={item.id} draggableId={String(item.id)} index={index}>
                                            {(provided) => (
                                                <Card
                                                    ref={provided.innerRef}
                                                    {...provided.draggableProps}
                                                    {...provided.dragHandleProps}
                                                    style={{ margin: 8 }}>
                                                    <CardContent>
                                                        <Typography>{item.name}</Typography>
                                                        <Typography color="textSecondary" gutterBottom>
                                                            {item.storeName}
                                                        </Typography>
                                                    </CardContent>
                                                </Card>
                                            )}
                                        </Draggable>
                                    ))}
                                    {provided.placeholder}
                                </Paper>
                            </Grid>
                        )}
                    </Droppable>
                ))}
            </Grid>
        </DragDropContext>
    );
};

export default KanbanBoard;
