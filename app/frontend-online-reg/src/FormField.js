import './App.css';

export default function FormField({
  fieldArea = '',
  label,
  htmlFor,
  children,
  error
}) {
  return (
    <div className={`form-field ${fieldArea}`}>
      <label htmlFor={htmlFor}>{label}</label>
      {children}
      {error && <span className='error-message'>{error}</span>}
    </div>
  );
}