import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    console.log('Dashboard handleLogout called');
    try {
      await logout();
      console.log('Dashboard logout completed, navigating to login');
      navigate('/login', { replace: true });
    } catch (error) {
      console.error('Dashboard logout error:', error);
      // Even if logout fails, redirect to login
      navigate('/login', { replace: true });
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card">
            <div className="card-header d-flex align-items-center">
              <img 
                src="/logo.svg" 
                alt="Auth System Logo" 
                width="40" 
                height="40"
                className="me-3"
              />
              <h3 className="mb-0">Dashboard</h3>
            </div>
            <div className="card-body">
              <div className="welcome-section">
                <h3>Welcome, {user?.username}!</h3>
                <p>You are successfully logged in to your account.</p>
                <p><strong>Email:</strong> {user?.email}</p>
              </div>
              
              <div className="actions mt-4">
                <Link to="/change-password" className="btn btn-warning me-3">
                  Change Password
                </Link>
                <button onClick={handleLogout} className="btn btn-danger">
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
