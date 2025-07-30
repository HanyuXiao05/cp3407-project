import { useState, useEffect } from 'react';
import PageLayout from './PageLayout';
import Modal from './Modal';
import { sessionApi } from '../services/sessionApi';
import styles from '../styles/SessionBooking.module.css';

const guidelines = [
  "Only registered gym members are allowed. No friends allowed.",
  "6 members per 1-hour timeslot. Max 2 hours per day per person.",
  "Advance booking required. Violations may result in a 2-week suspension.",
  "End session 10 minutes early for clean-up.",
  "Inspections by security staff may occur.",
  "Repeated no-shows or violations may result in revocation of access.",
  "JCU and staff are not responsible for personal belongings.",
  "Only water is allowed in the gym. No food or other drinks."
];

export default function SessionBookingPage() {
  const [userType, setUserType] = useState('student');
  const [date, setDate] = useState('');
  const [slotAvailability, setSlotAvailability] = useState([]);
  const [selectedSlots, setSelectedSlots] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [bookingDetails, setBookingDetails] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Mock member ID for demo purposes (in real app, this would come from authentication)
  const mockMemberId = 2304; // Using integer member ID

  useEffect(() => {
    if (!date) {
      setSlotAvailability([]);
      setSelectedSlots([]);
      return;
    }

    fetchSlotAvailability();
  }, [userType, date]);

  const fetchSlotAvailability = async () => {
    if (!date) return;

    setLoading(true);
    setError('');

    try {
      const data = await sessionApi.getSlotAvailability(date, userType);
      setSlotAvailability(data.slots || []);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Error fetching slot availability:', error);
      setError('Failed to load slot availability. Please try again.');
      setSlotAvailability([]);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchSlotAvailability();
  };

  const handleSlotChange = (slot) => {
    if (selectedSlots.includes(slot)) {
      setSelectedSlots(selectedSlots.filter(s => s !== slot));
    } else {
      if (selectedSlots.length >= 2) {
        return;
      }
      setSelectedSlots([...selectedSlots, slot]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!date || selectedSlots.length === 0) {
      setError('Please select a valid date and at least one time slot.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Book each selected slot
      const bookingPromises = selectedSlots.map(slot => 
        sessionApi.bookSlot({
          date: date,
          time_slot: slot,
          member_id: mockMemberId
        })
      );

      const results = await Promise.all(bookingPromises);
      
      setBookingDetails({
        userType: userType,
        date: date,
        timeSlots: selectedSlots,
        bookingRefs: results.map(r => r.booking_ref)
      });
      
      setBookingSuccess(true);
      setShowModal(true);
      setSelectedSlots([]);
      
      // Refresh availability after successful booking
      setTimeout(() => {
        fetchSlotAvailability();
      }, 1000);
      
    } catch (error) {
      console.error('Error booking slots:', error);
      setError(error.message || 'Booking failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSlotStatusClass = (slot) => {
    if (slot.is_full) return styles.full;
    if (slot.available_spots <= 2) return styles.limited;
    return styles.available;
  };

  const getSlotStatusText = (slot) => {
    if (slot.is_full) return 'Full';
    if (slot.available_spots <= 2) return `${slot.available_spots} spots left`;
    return `${slot.available_spots} spots available`;
  };

  const formatLastUpdated = () => {
    if (!lastUpdated) return '';
    return lastUpdated.toLocaleTimeString();
  };

  return (
    <PageLayout title="Book Your Gym Session">
      <div className={styles.bookingContainer}>
        <div className={styles.bookingCard}>
          <div className={styles.header}>
            <h2>📅 Session Booking</h2>
            <p>Select your preferred time slots for your gym session</p>
            <div className={styles.realTimeInfo}>
              <span className={styles.liveIndicator}>🟢</span>
              <span>Real-time availability (Max 6 people per session)</span>
              {lastUpdated && (
                <span className={styles.lastUpdated}>
                  Last updated: {formatLastUpdated()}
                </span>
              )}
            </div>
          </div>

          <form onSubmit={handleSubmit} className={styles.bookingForm}>
            <div className={styles.formSection}>
              <label htmlFor="userType" className={styles.label}>
                <span className={styles.labelIcon}>👤</span>
                Select User Type:
              </label>
              <select 
                id="userType" 
                value={userType} 
                onChange={e => {setUserType(e.target.value); setSelectedSlots([]);}}
                className={styles.select}
              >
                <option value="student">🎓 Student</option>
                <option value="staff">👨‍💼 Staff</option>
              </select>
            </div>

            <div className={styles.formSection}>
              <label htmlFor="date" className={styles.label}>
                <span className={styles.labelIcon}>📆</span>
                Session Date:
              </label>
              <input 
                type="date" 
                id="date" 
                value={date} 
                onChange={e => {setDate(e.target.value); setSelectedSlots([]);}}
                className={styles.dateInput}
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            <div className={styles.formSection}>
              <div className={styles.sectionHeader}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>⏰</span>
                  Available Time Slots:
                </label>
                {date && (
                  <button 
                    type="button" 
                    onClick={handleRefresh}
                    className={styles.refreshButton}
                    disabled={loading}
                  >
                    {loading ? '🔄' : '🔄'} Refresh
                  </button>
                )}
              </div>
              
              {loading && (
                <div className={styles.loading}>
                  <span>🔄</span>
                  <p>Loading real-time availability...</p>
                </div>
              )}

              {error && (
                <div className={styles.error}>
                  <span>⚠️</span>
                  <p>{error}</p>
                </div>
              )}

              <div className={styles.slotGrid}>
                {date && !loading ? (
                  slotAvailability.length > 0 ? (
                    slotAvailability.map((slot, i) => (
                      <div 
                        key={slot.time_slot} 
                        className={`${styles.slotItem} ${getSlotStatusClass(slot)} ${selectedSlots.includes(slot.time_slot) ? styles.selected : ''}`}
                        onClick={() => !slot.is_full && handleSlotChange(slot.time_slot)}
                      >
                        <div className={styles.slotHeader}>
                          <input
                            type="checkbox"
                            id={`slot-${i}`}
                            name="timeSlot"
                            value={slot.time_slot}
                            checked={selectedSlots.includes(slot.time_slot)}
                            onChange={() => !slot.is_full && handleSlotChange(slot.time_slot)}
                            disabled={slot.is_full || (!selectedSlots.includes(slot.time_slot) && selectedSlots.length >= 2)}
                            className={styles.checkbox}
                          />
                          <label htmlFor={`slot-${i}`} className={styles.slotLabel}>
                            {slot.time_slot}
                          </label>
                        </div>
                        
                        <div className={styles.slotDetails}>
                          <div className={styles.availabilityInfo}>
                            <span className={styles.availabilityText}>
                              {getSlotStatusText(slot)}
                            </span>
                            <div className={styles.capacityBar}>
                              <div 
                                className={styles.capacityFill} 
                                style={{ width: `${slot.percentage_full}%` }}
                              ></div>
                            </div>
                          </div>
                          
                          <div className={styles.bookingStats}>
                            <span className={styles.bookedCount}>
                              {slot.booked_count}/6 booked
                            </span>
                            <span className={styles.percentage}>
                              {slot.percentage_full}% full
                            </span>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className={styles.noSlots}>
                      <span>📭</span>
                      <p>No available slots on this day.</p>
                    </div>
                  )
                ) : (
                  <div className={styles.selectDate}>
                    <span>📅</span>
                    <p>Please select a date to view available slots</p>
                  </div>
                )}
              </div>
            </div>

            <div className={styles.selectedInfo}>
              {selectedSlots.length > 0 && (
                <div className={styles.selectedSlots}>
                  <span>✅ Selected: {selectedSlots.join(', ')}</span>
                  <span className={styles.slotCount}>({selectedSlots.length}/2 slots)</span>
                </div>
              )}
            </div>

            <button 
              type="submit" 
              className={styles.submitButton}
              disabled={loading || selectedSlots.length === 0}
            >
              {loading ? '🔄 Processing...' : '🎯 Confirm Booking'}
            </button>
          </form>
        </div>

        <div className={styles.guidelinesCard}>
          <h3>📋 Gym Guidelines</h3>
          <ul className={styles.guidelinesList}>
            {guidelines.map((guideline, i) => (
              <li key={i} className={styles.guidelineItem}>
                {guideline}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {showModal && bookingSuccess && (
        <Modal title="🎉 Booking Confirmed!" onClose={() => setShowModal(false)}>
          <div className={styles.confirmationContent}>
            <div className={styles.successIcon}>✅</div>
            <h3>Your booking has been successfully confirmed!</h3>
            <div className={styles.bookingDetails}>
              <p><strong>User Type:</strong> {bookingDetails.userType}</p>
              <p><strong>Date:</strong> {bookingDetails.date}</p>
              <p><strong>Time Slots:</strong> {bookingDetails.timeSlots.join(', ')}</p>
              <p><strong>Booking References:</strong> {bookingDetails.bookingRefs.join(', ')}</p>
            </div>
            <div className={styles.bookingInstructions}>
              <p>📋 Please remember:</p>
              <ul>
                <li>Arrive 5 minutes before your scheduled time</li>
                <li>Bring your student/staff ID</li>
                <li>Follow all gym guidelines</li>
                <li>End session 10 minutes early for clean-up</li>
              </ul>
            </div>
          </div>
        </Modal>
      )}
    </PageLayout>
  );
} 