import styles from '../styles/Registration.module.css';

export default function RegistrationFormField({
  fieldArea = '',
  label,
  htmlFor,
  children,
  error
}) {
  return (
    <div className={`${styles.formField} ${fieldArea}`}>
      <label htmlFor={htmlFor}>{label}</label>
      {children}
      {error && <span className={styles.errorMessage}>{error}</span>}
    </div>
  );
}