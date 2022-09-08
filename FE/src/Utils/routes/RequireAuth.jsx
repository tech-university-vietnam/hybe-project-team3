import React from 'react';
import PropTypes from 'prop-types';
import useAuth from '../hooks/auth.js';
import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }) => {
    const { authed, isLoading } = useAuth();
    return isLoading ? <></> : authed !== null ? children : <Navigate to="/login" replace />;
}

RequireAuth.propTypes = {
}

export default RequireAuth