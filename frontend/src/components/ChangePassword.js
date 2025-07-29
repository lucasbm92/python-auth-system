import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const ChangePassword = () => {
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { changePassword } = useAuth();
  const navigate = useNavigate();

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

    const result = await changePassword(formData);
    
    if (result.success) {
      alert('Password changed successfully!');
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <div className="text-center mb-4">
                <img 
                  className="mb-3" 
                  src="/logo.svg" 
                  alt="Auth System Logo" 
                  width="72" 
                  height="72"
                />
                <h2 className="card-title">Change Password</h2>
              </div>
              
              {error && (
                <div className="alert alert-danger">{error}</div>
              )}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="current_password" className="form-label">Current Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="current_password"
                    name="current_password"
                    value={formData.current_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label htmlFor="new_password" className="form-label">New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="new_password"
                    name="new_password"
                    value={formData.new_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label htmlFor="confirm_password" className="form-label">Confirm New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="confirm_password"
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <button 
                  type="submit" 
                  className="btn btn-primary w-100"
                  disabled={loading}
                >
                  {loading ? 'Changing Password...' : 'Change Password'}
                </button>
              </form>
              
              <div className="text-center mt-3">
                <Link to="/dashboard">← Back to Dashboard</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword;
