import styles from '../styles/PageLayout.module.css';

export default function PageLayout({
  title,
  children
}) {
  return (
    <>
      <div className='divider' />
      <div className={styles.App}>
        {title && <h1>{title}</h1>}
        <fieldset>{children}</fieldset>
      </div>
    </>
  );
}
