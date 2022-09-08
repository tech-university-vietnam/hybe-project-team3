import React from "react";
import PropTypes from "prop-types";
import LoginForm from "components/LoginForm/LoginForm";
import useAuth from "../../Utils/hooks/auth";
import { Navigate } from 'react-router-dom';

const Login = () => {
  const { authed, isLoading } = useAuth();

  return isLoading ? <></> : authed ? <Navigate to="/" replace /> : <LoginForm />;
};

Login.propTypes = {};

export default Login;
