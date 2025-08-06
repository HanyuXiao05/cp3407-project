import styles from '../styles/Modal.module.css';

export default function Modal({
  title,
  children,
  onClose
}) {
  return (
    <div className={styles.overlay}>
      <div className={styles.box}>
        {title && <h2>{title}</h2>}
        {children}
        <div className={`divider ${styles.modalDivider}`} />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}