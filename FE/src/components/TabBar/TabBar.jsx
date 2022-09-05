import React from 'react'
import PropTypes from 'prop-types'
import { Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography } from '@mui/material'
import InventoryIcon from '@mui/icons-material/Inventory'
import FactCheckIcon from '@mui/icons-material/FactCheck'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'

const TabBar = () => {
    return (
        <Box
            sx={{
                width: '15vw',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                borderRight: '1px solid #C4C4C4',
                // bgcolor: 'background.paper'
            }}>
            <nav>
                <List
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '1rem'
                    }}
                >
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <InventoryIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold'
                                        }}>
                                        TRACKED LIST
                                    </Typography>
                                }
                            />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <FactCheckIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold'
                                        }}>
                                        WISH LIST
                                    </Typography>
                                }
                            />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <NotificationsActiveIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold'
                                        }}>
                                        NOTIFICATION
                                    </Typography>
                                }
                            />
                        </ListItemButton>
                    </ListItem>
                </List>
            </nav>
        </Box >
    )
}

TabBar.propTypes = {}

export default TabBar