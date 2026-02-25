import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import Login from "./pages/LoginPage";
import Dashboard from "./pages/DashboardPage";
import Setting from "./pages/SettingPage";
import History from "./pages/HistoryPage";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Login />,
    },
    {
        path: '/dashboard',
        element: <ProtectedRoute><Dashboard /></ProtectedRoute>
    },
    {
        path: '/setting',
        element: <ProtectedRoute><Setting /></ProtectedRoute>
    },
    {
        path: '/history',
        element: <ProtectedRoute><History /></ProtectedRoute>
    }
]);

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<RouterProvider router={router} />);
