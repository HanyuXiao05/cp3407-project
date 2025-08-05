import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import PageLayout from './PageLayout';
import styles from '../styles/Login.module.css';
import { loginMember } from '../services/api';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (formData.email && formData.password) {
        const response = await loginMember({
          email: formData.email,
          password: formData.password
        });

        const userData = response.data.member;
        
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Navigate to booking page
        navigate('/booking');
      } else {
        setError('Please fill in all fields');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.error || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout>
      <div className={styles.loginContainer}>
        <div className={styles.loginCard}>
          <div className={styles.header}>
            <h1>🔐 Welcome Back</h1>
            <p>Sign in to your gym account</p>
          </div>

          <form onSubmit={handleSubmit} className={styles.loginForm}>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter your email"
                required
                className={styles.input}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Enter your password"
                required
                className={styles.input}
              />
            </div>

            {error && (
              <div className={styles.error}>
                ❌ {error}
              </div>
            )}

            <button 
              type="submit" 
              className={styles.loginButton}
              disabled={loading}
            >
              {loading ? '🔄 Signing in...' : '🚀 Sign In'}
            </button>
          </form>

          <div className={styles.divider}>
            <span>or</span>
          </div>

          <div className={styles.alternateAction}>
            <p>Don't have an account?</p>
            <Link to="/" className={styles.registerLink}>
              📝 Create New Account
            </Link>
          </div>

          <div className={styles.features}>
            <h3>🎯 Quick Access Features</h3>
            <ul>
              <li>✅ Direct booking access</li>
              <li>📅 View your booking history</li>
              <li>⚡ Faster session booking</li>
              <li>🔒 Secure account management</li>
            </ul>
          </div>
        </div>
      </div>
    </PageLayout>
  );
} 