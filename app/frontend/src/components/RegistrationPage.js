import React from 'react';
import { Link } from 'react-router-dom';
import PageLayout from './PageLayout';
import RegistrationForm from './RegistrationForm';

export default function RegistrationPage() {
  return (
    <PageLayout title='JCU GYM MEMBERSHIP REGISTRATION'>
      <fieldset>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <p style={{ color: '#666', marginBottom: '10px' }}>
            Already have an account?
          </p>
          <Link 
            to="/login" 
            style={{
              display: 'inline-block',
              padding: '10px 20px',
              background: '#172DD5',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: '600',
              transition: 'background-color 0.3s ease'
            }}
          >
            🔐 Sign In Instead
          </Link>
        </div>
      <RegistrationForm />
      </fieldset>
    </PageLayout>
  );
}