import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFound() {
    return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center p-4 text-center">
            <h1 className="text-4xl font-bold text-gray-300 mb-4">404</h1>
            <p className="text-xl text-gray-600 mb-8">Page Not Found</p>
            <Link to="/" className="text-blue-600 hover:text-blue-800 hover:underline">
                Return to Home
            </Link>
        </div>
    );
}
