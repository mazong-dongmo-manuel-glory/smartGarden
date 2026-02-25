import React from 'react';
import Header from './Header';
import Footer from './Footer';

const Layout = ({ children }) => {
    return (
        <div className="bg-gray-950 text-gray-100 font-sans min-h-screen flex flex-col">
            <Header />
            <main className="flex-grow max-w-[1440px] w-full mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8 overflow-x-hidden">
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
