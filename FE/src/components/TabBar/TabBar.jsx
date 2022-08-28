import React from 'react'
import PropTypes from 'prop-types'
import { Box, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material'
import InventoryIcon from '@mui/icons-material/Inventory'
import FactCheckIcon from '@mui/icons-material/FactCheck'
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive'

const TabBar = props => {
    return (
        <Box sx={{
            width: '100%',
            maxWidth: 360,
            // bgcolor: 'background.paper'
        }}>
            <nav>
                <List>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <InventoryIcon />
                            </ListItemIcon>
                            <ListItemText primary="Inventory" />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <FactCheckIcon />
                            </ListItemIcon>
                            <ListItemText primary="Wishlist" />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <NotificationsActiveIcon />
                            </ListItemIcon>
                            <ListItemText primary="Notification" />
                        </ListItemButton>
                    </ListItem>
                </List>
            </nav>
        </Box>
    )
}

TabBar.propTypes = {}

export default TabBar