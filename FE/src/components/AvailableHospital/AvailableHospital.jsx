import React from 'react'
import PropTypes from 'prop-types';
import { Button, Card, CardContent, Grid, Typography } from '@mui/material';
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import CallIcon from '@mui/icons-material/Call';
import BusinessIcon from '@mui/icons-material/Business';
import { Box } from '@mui/system';

const AvailableHospital = ({ id, hospital, expired, contact, address }) => {
    const onApprove = ({ id }) => {

    }
    const onDecline = ({ id }) => {

    }
    return (
        <Card>
            <CardContent sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <Typography sx={{ fontWeight: 'bold' }}>{hospital}</Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <Box>
                        <Grid container>
                            {/* <Grid item xs={6}>
                                <Typography>Expired date:</Typography>
                            </Grid>
                            <Grid item xs={6}>
                                <Typography>{expired}</Typography>
                            </Grid> */}
                            <Grid item xs={1}>
                                <Typography><CallIcon /></Typography>
                            </Grid>
                            <Grid item xs={11}>
                                <Typography>{contact}</Typography>
                            </Grid>
                            <Grid item xs={1}>
                                <Typography><BusinessIcon/></Typography>
                            </Grid>
                            <Grid item xs={11}>
                                <Typography>{address}</Typography>
                            </Grid>
                        </Grid>
                    </Box>
                    <Box sx={{ display: 'flex', jutifyContent: 'center', marginLeft: 'auto', marginRight: 0, gap: '1rem', height: '100%' }}>
                        <Button onClick={() => onDecline({ id })} startIcon={<CloseIcon />}>
                            Decline
                        </Button>
                        <Button onClick={() => onApprove({ id })} startIcon={<CheckIcon />}>
                            Buy
                        </Button>
                    </Box>
                </Box>

            </CardContent>
        </Card>
    )
}

AvailableHospital.propTypes = {
    name: PropTypes.string,
    expiredDate: PropTypes.string,
    phone: PropTypes.string
}

export default AvailableHospital