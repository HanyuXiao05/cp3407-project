import { useLocation, Link } from 'react-router-dom'
import styles from '../styles/PageLayout.module.css';

export default function PageLayout({
  title,
  children
}) {
  const location = useLocation();
  const pathname = location.pathname;

  const showVirtualTourButton = pathname === '/' || pathname === '/login';
  const showLoginButton = pathname === '/' || pathname === '/tour';
  const showRegisterButton = pathname === '/login';
  const showLogoutButton = pathname === '/admin' || pathname === '/booking';

  const logout = () => {
    window.location.href = '/login';
  };

  return (
    <>
      <header className={styles.header}>
        <div className={styles.buttonGroup}>
          {showVirtualTourButton && (
            <Link to='/tour'>
              <button type='button'>Virtual Gym Tour</button>
            </Link>
          )}

          {showLogoutButton ? (
            <button type='button' onClick={logout}>Log Out</button>
          ) : showRegisterButton ? (
            <Link to='/'>
              <button type='button'>Register</button>
            </Link>
          ) : showLoginButton ? (
            <Link to='/login'>
              <button type='button'>Log In</button>
            </Link>
          ) : null}         
        </div>
      </header>
      <div className={`divider ${styles.pageDivider}`} />
      <div className={styles.content}>
        {title && <h1>{title}</h1>}
        {children}
      </div>
    </>
  );
}
