import React from 'react';
import Header from './Header';
import Footer from './Footer';

const Layout = ({ children }) => {
    return (
        <div className="bg-gray-950 text-gray-100 font-sans min-h-screen flex flex-col">
            <Header />
            <main className="flex-grow max-w-[1440px] w-full mx-auto px-8 py-8">
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
