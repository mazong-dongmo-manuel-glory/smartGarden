import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import Login from "./pages/LoginPage";
import Dashboard from "./pages/DashboardPage";
import Setting from "./pages/SettingPage";
import History from "./pages/HistoryPage";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Login />,
    },
    {
        path: '/dashboard',
        element: <Dashboard />
    },
    {
        path: '/setting',
        element: <Setting />
    },
    {
        path: '/history',
        element: <History />
    }
]);

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<RouterProvider router={router} />);
