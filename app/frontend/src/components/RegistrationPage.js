import React from 'react';
import { Link } from 'react-router-dom';
import PageLayout from './PageLayout';
import RegistrationForm from './RegistrationForm';
import styles from '../styles/Registration.module.css';

export default function RegistrationPage() {
  return (
    <PageLayout title='JCU GYM MEMBERSHIP REGISTRATION'>
      <fieldset>
        <div className={styles.headerContainer}>
          <p className={styles.offlineNote}>
            ⚠️ Please note: Offline payment must be made at the counter.
          </p>

          <p className={styles.signInPrompt}>
            Already have an account?
          </p>

          <Link to="/login" className={styles.signInButton}>
            🔐 Sign In Instead
          </Link>
        </div>
      <RegistrationForm />
      </fieldset>
    </PageLayout>
  );
}