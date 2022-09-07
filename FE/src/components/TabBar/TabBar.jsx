import React from 'react'
import PropTypes from 'prop-types'
import { Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography } from '@mui/material'
import InventoryIcon from '@mui/icons-material/Inventory'
import FactCheckIcon from '@mui/icons-material/FactCheck'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'

const TabBar = ({ currentTab, handleChangeTab }) => {
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
                    <ListItem
                        disablePadding
                        sx={{
                            backgroundColor: currentTab === 'tracked-list' ? '#0079D8' : 'none',
                        }}
                    >
                        <ListItemButton onClick={() => handleChangeTab('tracked-list')}>
                            <ListItemIcon>
                                <InventoryIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold',
                                            color: currentTab === 'tracked-list' ? 'white' : 'black'
                                        }}>
                                        TRACKED LIST
                                    </Typography>
                                }
                            />
                        </ListItemButton>
                    </ListItem>
                    <ListItem
                        disablePadding
                        sx={{
                            backgroundColor: currentTab === 'wishlist' ? '#0079D8' : 'none',
                        }}
                    >
                        <ListItemButton onClick={() => handleChangeTab('wishlist')}>
                            <ListItemIcon>
                                <FactCheckIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold',
                                            color: currentTab === 'wishlist' ? 'white' : 'black'
                                        }}>
                                        WISH LIST
                                    </Typography>
                                }
                            />
                        </ListItemButton>
                    </ListItem>
                    <ListItem
                        disablePadding
                        sx={{
                            backgroundColor: currentTab === 'notification' ? '#0079D8' : 'none',
                        }}
                    >
                        <ListItemButton onClick={() => handleChangeTab('notification')}>
                            <ListItemIcon>
                                <NotificationsActiveIcon />
                            </ListItemIcon>
                            <ListItemText
                                primary={
                                    <Typography
                                        style={{
                                            fontWeight: 'bold',
                                            color: currentTab === 'notification' ? 'white' : 'black'
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

TabBar.propTypes = {
    handleChangeTab: PropTypes.func
}

export default TabBar