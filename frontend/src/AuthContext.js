import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from './api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    console.log('Checking auth status...');
    
    // First, check if there's a user in localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        console.log('Found stored user data:', userData);
        setUser(userData);
      } catch (error) {
        console.log('Error parsing stored user data:', error);
        localStorage.removeItem('user');
      }
    }
    
    // Always set loading to false after checking localStorage
    // Don't wait for server verification to complete
    setLoading(false);
    
    // Then try to verify with the server (in background)
    try {
      const response = await authAPI.getProfile();
      console.log('Auth check successful, user:', response.data);
      setUser(response.data);
      // Store user data in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (error) {
      console.log('Auth check failed:', error.response?.status, error.response?.data);
      // Only clear stored user if we get a specific 401 (unauthorized) error
      // 403 might just mean session expired but user data is still valid for UI purposes
      if (error.response?.status === 401) {
        console.log('Clearing invalid stored user data due to 401');
        setUser(null);
        localStorage.removeItem('user');
      }
      // For 403 or other errors, keep the stored user data for UI consistency
    }
  };

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials);
      const userData = response.data.user;
      setUser(userData);
      // Store user data in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(userData));
      return { success: true, data: response.data };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data || 'Registration failed' 
      };
    }
  };

  const logout = async () => {
    console.log('Logout function called');
    try {
      // First make the API call to logout
      console.log('Making API logout call...');
      await authAPI.logout();
      console.log('Logout API call successful');
    } catch (error) {
      console.log('Logout API call failed, but continuing with logout:', error);
    }
    
    // Always clear user state and cached data
    console.log('Clearing user state and storage...');
    setUser(null);
    localStorage.removeItem('user');
    sessionStorage.clear();
    
    console.log('Logout state cleared');
    return { success: true };
  };

  const changePassword = async (passwordData) => {
    try {
      const response = await authAPI.changePassword(passwordData);
      return { success: true, data: response.data };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Password change failed' 
      };
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    changePassword,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
