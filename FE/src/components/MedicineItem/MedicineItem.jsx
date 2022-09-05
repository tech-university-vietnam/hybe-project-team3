import React from 'react'
import PropTypes from 'prop-types'
import { Button, Card, CardContent, CardHeader, Grid, IconButton, Typography } from '@mui/material'
import VaccinesIcon from '@mui/icons-material/Vaccines'
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';

const MedicineItem = ({name, expirationDate}) => {
    return (
        <Card sx={{ width: 1 }}>
            <CardHeader
                avatar={
                    <VaccinesIcon />
                }
                title={name}
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
                        <Typography variant="body1">Expired date: {expirationDate}</Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <Button variant="contained" sx={{bgcolor: 'green'}}>Status</Button>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    )
}

MedicineItem.propTypes = {
    name: PropTypes.string,
    exp: PropTypes.string
}

export default MedicineItem