import { useState } from 'react';
import PageLayout from './PageLayout';
import styles from '../styles/VirtualTour.module.css';

export default function VirtualTourPage() {
  const [expanded, setExpanded] = useState(false);

  const handleHotspotClick = () => {
    setExpanded(true);
  };

  const handleClose = () => {
    setExpanded(false);
  };

  return (
    <PageLayout title='VIRTUAL GYM TOUR'>
      <div className={styles.virtualTourContainer}>
        <div className={styles.mapContainer}>
          <img
            src='/gym-location.png'
            alt='Gym Location'
            className={styles.gymLocation}
          />
          <button
            className={styles.mapHotspot}
            onClick={handleHotspotClick}
            aria-label='Enter the gym'
          />
        </div>

        {expanded && (
          <div className={styles.interiorOverlay} onClick={handleClose}>
            <div
              className={styles.interiorContainer}
              onClick={e => e.stopPropagation()}
            >
              <img
                src='/gym-interior.jpeg'
                alt='Gym Interior'
                className={styles.gymInterior}
              />
            </div>
            <button className={styles.closeButton} onClick={handleClose} aria-label='Close'>
              ×
            </button>
          </div>
        )}
      </div>
    </PageLayout>
  );
}