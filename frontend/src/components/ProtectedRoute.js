import React from 'react';
import { Navigate } from 'react-router-dom';

// Simple Auth Wrap — checks localStorage
export default function ProtectedRoute({ children }) {
    const isAuthenticated = localStorage.getItem('smartgarden_auth') === 'true';

    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }

    return children;
}
