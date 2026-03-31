/**
 * AuthGuard.jsx - Authentication placeholder component
 * 
 * TODO: Implement real authentication
 * - Connect to auth service
 * - Handle login/logout
 * - Store JWT token in localStorage or Cookie
 * - Redirect to login if not authenticated
 * - Handle token refresh
 */

import React, { useState, useEffect } from 'react';

/**
 * AuthGuard component that wraps protected routes
 * 
 * Usage:
 * <AuthGuard>
 *   <MyProtectedComponent />
 * </AuthGuard>
 */
export const AuthGuard = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState(null);

  // TODO: Replace with real authentication check
  useEffect(() => {
    // Simulate auth check
    setTimeout(() => {
      // Check for token in localStorage
      const token = localStorage.getItem('authToken');
      if (token) {
        setIsAuthenticated(true);
        // TODO: Decode token to get user info
        setUser({ id: 'user_placeholder', email: 'user@example.com' });
      }
      setIsLoading(false);
    }, 500);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center max-w-md mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">WeTransfer Clone</h1>
          <p className="text-gray-600 mb-8">
            Please log in to continue
          </p>
          
          {/* TODO: Add real login form */}
          <div className="bg-white p-8 rounded-lg shadow-md">
            <button
              onClick={() => {
                // Placeholder: set token for demo
                localStorage.setItem('authToken', 'demo-token-' + Date.now());
                setIsAuthenticated(true);
                // TODO: Call real auth service
              }}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition"
            >
              Demo Login
            </button>
            <p className="text-xs text-gray-500 mt-4">
              TODO: Implement real authentication with OAuth/Email
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Authenticated - render children
  return children;
};

export default AuthGuard;
