import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  const { login, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Check for success message from navigation state
  useEffect(() => {
    if (location.state?.successMessage) {
      setSuccessMessage(location.state.successMessage);
      // Clear the message from history state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate]);

  // Redirect to dashboard if user is already logged in
  useEffect(() => {
    console.log('Login useEffect - authLoading:', authLoading, 'user:', user);
    console.log('localStorage user:', localStorage.getItem('user'));
    if (!authLoading && user) {
      console.log('Redirecting to dashboard...');
      navigate('/dashboard', { replace: true });
    }
  }, [user, authLoading, navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMessage('');

    const result = await login(formData);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  // Show loading while checking authentication status
  if (authLoading) {
    return (
      <div className="d-flex align-items-center justify-content-center py-4 bg-body-tertiary" style={{ minHeight: '100vh' }}>
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Checking authentication...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="d-flex align-items-center justify-content-center py-4 bg-body-tertiary" style={{ minHeight: '100vh' }}>
      <main className="form-signin w-100 m-auto" style={{ maxWidth: '330px' }}>
        {successMessage && (
          <div className="alert alert-success alert-dismissible fade show">
            {successMessage}
            <button 
              type="button" 
              className="btn-close" 
              onClick={() => setSuccessMessage('')}
              aria-label="Close"
            ></button>
          </div>
        )}
        
        {error && (
          <div className="alert alert-danger">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="text-center mb-4">
            <img 
              className="mb-4" 
              src="/logo.svg" 
              alt="Auth System Logo" 
              width="72" 
              height="72"
            />
            <h1 className="h3 mb-3 fw-normal">Please sign in</h1>
          </div>
          
          <div className="form-floating">
            <input
              type="email"
              className="form-control"
              id="floatingInput"
              name="email"
              placeholder="name@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <label htmlFor="floatingInput">Email address</label>
          </div>
          
          <div className="form-floating">
            <input
              type="password"
              className="form-control"
              id="floatingPassword"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <label htmlFor="floatingPassword">Password</label>
          </div>

          <div className="form-check my-3">
            <input
              className="form-check-input"
              type="checkbox"
              id="rememberMe"
            />
            <label className="form-check-label" htmlFor="rememberMe">
              Remember me
            </label>
          </div>
          
          <button 
            className="btn btn-primary w-100 py-2" 
            type="submit"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
          
          <div className="links mt-3 text-center">
            <p>Don't have an account? <Link to="/register">Register</Link></p>
            <Link to="/forgot-password">Forgot your password?</Link>
          </div>
          
          <p className="mt-3 mb-3 text-body-secondary text-center">&copy; 2017–2025</p>
        </form>
      </main>
    </div>
  );
};

export default Login;
