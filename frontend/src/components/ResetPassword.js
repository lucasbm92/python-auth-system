import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../AuthContext';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    new_password: '',
    confirm_password: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState('');

  useEffect(() => {
    const tokenFromUrl = searchParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    } else {
      setError('Invalid or missing reset token');
    }
  }, [searchParams]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    // Validate passwords match
    if (formData.new_password !== formData.confirm_password) {
      setError('Passwords do not match');
      return;
    }

    // Validate password strength
    if (formData.new_password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (!token) {
      setError('Invalid reset token');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/reset-password/', {
        token: token,
        new_password: formData.new_password
      });

      setMessage('Password has been reset successfully! You can now login with your new password.');
      setFormData({ new_password: '', confirm_password: '' });
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);

    } catch (error) {
      setError(error.response?.data?.error || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header text-center bg-primary text-white">
              <h4>Reset Password</h4>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}
              
              {message && (
                <div className="alert alert-success" role="alert">
                  {message}
                </div>
              )}

              {!message && token && (
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="new_password" className="form-label">
                      New Password
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="new_password"
                      name="new_password"
                      value={formData.new_password}
                      onChange={handleChange}
                      required
                      minLength="6"
                      placeholder="Enter your new password"
                    />
                  </div>
                  
                  <div className="mb-3">
                    <label htmlFor="confirm_password" className="form-label">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="confirm_password"
                      name="confirm_password"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      required
                      minLength="6"
                      placeholder="Confirm your new password"
                    />
                  </div>
                  
                  <button 
                    type="submit" 
                    className="btn btn-primary w-100"
                    disabled={loading}
                  >
                    {loading ? 'Resetting...' : 'Reset Password'}
                  </button>
                </form>
              )}

              {!token && (
                <div className="text-center">
                  <p>Invalid or missing reset token.</p>
                  <Link to="/forgot-password" className="btn btn-link">
                    Request a new password reset
                  </Link>
                </div>
              )}

              <div className="text-center mt-3">
                <Link to="/login" className="text-decoration-none">
                  Back to Login
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
