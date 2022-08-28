import React from 'react'
import PropTypes from 'prop-types'
import './MedicineItem.css'
import { Button, Card, CardContent, CardHeader, Grid, IconButton, Typography } from '@mui/material'
import VaccinesIcon from '@mui/icons-material/Vaccines'
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';

const MedicineItem = props => {
    return (
        <Card sx={{ width: '70rem' }}>
            <CardHeader
                avatar={
                    <VaccinesIcon />
                }
                title={"Sinovac"}
                titleTypographyProps={{ variant: 'h6' }}
                action={
                    <IconButton>
                        <DeleteSweepIcon sx={{ color: 'red' }} />
                    </IconButton>
                }
            />
            <CardContent>
                <Grid container direction="row">
                    <Grid item xs={11}>
                        <Typography variant="body1">Expired date: {"20/10/2030"}</Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <Button variant="contained" sx={{bgcolor: 'green'}}>Status</Button>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    )
}

MedicineItem.propTypes = {}

export default MedicineItem