import React from 'react';
import PropTypes from 'prop-types';
import useAuth from '../hooks/auth.js';
import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }) => {
    const { authed } = useAuth();

    return authed === true ? children : <Navigate to="/login" replace />;
}

RequireAuth.propTypes = {
}

export default RequireAuth