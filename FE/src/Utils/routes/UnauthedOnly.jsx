import React from 'react';
import PropTypes from 'prop-types';
import useAuth from "../../Utils/hooks/auth";
import { Navigate } from 'react-router-dom';

const UnauthedOnly = ({ children }) => {
    const { authed, isLoading } = useAuth();

    return isLoading ? <></> : authed === null ? children : <Navigate to="/" replace />;
}

UnauthedOnly.propTypes = {
}

export default UnauthedOnly