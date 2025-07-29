import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  
  const { register, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  // Redirect to dashboard if user is already logged in
  useEffect(() => {
    if (!authLoading && user) {
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
    setErrors({});

    const result = await register(formData);
    
    if (result.success) {
      // Navigate to login with success message
      navigate('/login', { 
        state: { 
          successMessage: 'Registration successful! Please log in with your new account.' 
        } 
      });
    } else {
      setErrors(result.error);
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
    <div className="bg-body-tertiary">
      <div className="container">
        <main>
          <div className="py-5 text-center">
            <img 
              className="mb-4" 
              src="/logo.svg" 
              alt="Auth System Logo" 
              width="72" 
              height="72"
            />
            <h1 className="h2">Registration</h1>
          </div>
          
          <div className="row g-5 justify-content-center">
            <div className="col-md-7 col-lg-8">
              {errors.non_field_errors && (
                <div className="alert alert-danger">
                  {errors.non_field_errors.map((error, index) => (
                    <div key={index}>{error}</div>
                  ))}
                </div>
              )}

              <form onSubmit={handleSubmit} className="needs-validation">
                <div className="row g-3">
                  <div className="col-12">
                    <label htmlFor="username" className="form-label">Username</label>
                    <div className="input-group has-validation">
                      <span className="input-group-text">@</span>
                      <input
                        type="text"
                        name="username"
                        className={`form-control ${errors.username ? 'is-invalid' : ''}`}
                        id="username"
                        placeholder="noobmaster69"
                        value={formData.username}
                        onChange={handleChange}
                        required
                      />
                      {errors.username && (
                        <div className="invalid-feedback">
                          {errors.username[0]}
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="col-12">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      name="email"
                      className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                      id="email"
                      placeholder="you@example.com"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                    {errors.email && (
                      <div className="invalid-feedback">
                        {errors.email[0]}
                      </div>
                    )}
                  </div>
                  
                  <div className="col-12">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                      type="password"
                      name="password"
                      className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                      id="password"
                      placeholder="Password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                    />
                    {errors.password && (
                      <div className="invalid-feedback">
                        {errors.password[0]}
                      </div>
                    )}
                  </div>
                  
                  <div className="col-12">
                    <label htmlFor="confirm_password" className="form-label">Confirm Password</label>
                    <input
                      type="password"
                      name="confirm_password"
                      className={`form-control ${errors.confirm_password ? 'is-invalid' : ''}`}
                      id="confirm_password"
                      placeholder="Confirm Password"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      required
                    />
                    {errors.confirm_password && (
                      <div className="invalid-feedback">
                        {errors.confirm_password[0]}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="d-flex justify-content-center gap-3 mt-4">
                  <button 
                    className="btn btn-primary btn-lg px-5" 
                    type="submit"
                    disabled={loading}
                  >
                    {loading ? 'Signing up...' : 'Sign Up'}
                  </button>
                  <Link to="/login" className="btn btn-secondary btn-lg px-5">
                    Cancel
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </main>
        
        <footer className="my-5 pt-5 text-body-secondary text-center text-small">
          <p className="mb-1">&copy; 2017–2025 Company Name</p>
        </footer>
      </div>
    </div>
  );
};

export default Register;
