import { useState, useEffect } from 'react';
import PageLayout from './PageLayout';
import Modal from './Modal';
import styles from '../styles/SessionBooking.module.css';

const staffHours = {
  Monday: [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  Tuesday: [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  Wednesday: [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  Thursday: [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  Friday: [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  Saturday: [["07:00", "13:00"]],
};

const studentHours = {
  Monday: [["08:00", "22:00"]],
  Tuesday: [["08:00", "22:00"]],
  Wednesday: [["08:00", "22:00"]],
  Thursday: [["08:00", "22:00"]],
  Friday: [["08:00", "22:00"]],
  Saturday: [["08:00", "18:00"]],
};

function timeToMinutes(t) {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
}

function minutesToTime(m) {
  const h = Math.floor(m / 60).toString().padStart(2, '0');
  const min = (m % 60).toString().padStart(2, '0');
  return `${h}:${min}`;
}

function getDayOfWeek(dateString) {
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  return days[new Date(dateString).getDay()];
}

function generateSlots(ranges) {
  const slots = [];
  for (const [start, end] of ranges) {
    let s = timeToMinutes(start);
    const e = timeToMinutes(end);
    while (s + 60 <= e) {
      const from = minutesToTime(s);
      const to = minutesToTime(s + 60);
      slots.push(`${from} - ${to}`);
      s += 60;
    }
  }
  return slots;
}

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
  const [slots, setSlots] = useState([]);
  const [selectedSlots, setSelectedSlots] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    if (!date) {
      setSlots([]);
      return;
    }
    const day = getDayOfWeek(date);
    const ranges = userType === 'staff' ? staffHours[day] : studentHours[day];
    if (!ranges) {
      setSlots([]);
      return;
    }
    setSlots(generateSlots(ranges));
  }, [userType, date]);

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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!date || selectedSlots.length === 0) {
      alert('Please select a valid date and at least one time slot.');
      return;
    }
    setShowModal(true);
  };

  return (
    <PageLayout title="Book Your Gym Session">
      <div className={styles.bookingContainer}>
        <div className={styles.bookingCard}>
          <div className={styles.header}>
            <h2>📅 Session Booking</h2>
            <p>Select your preferred time slots for your gym session</p>
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
              />
            </div>

            <div className={styles.formSection}>
              <label className={styles.label}>
                <span className={styles.labelIcon}>⏰</span>
                Available Time Slots:
              </label>
              <div className={styles.slotGrid}>
                {date ? (
                  slots.length > 0 ? (
                    slots.map((slot, i) => (
                      <div 
                        key={slot} 
                        className={`${styles.slotItem} ${selectedSlots.includes(slot) ? styles.selected : ''}`}
                        onClick={() => handleSlotChange(slot)}
                      >
                        <input
                          type="checkbox"
                          id={`slot-${i}`}
                          name="timeSlot"
                          value={slot}
                          checked={selectedSlots.includes(slot)}
                          onChange={() => handleSlotChange(slot)}
                          disabled={!selectedSlots.includes(slot) && selectedSlots.length >= 2}
                          className={styles.checkbox}
                        />
                        <label htmlFor={`slot-${i}`} className={styles.slotLabel}>
                          {slot}
                        </label>
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

            <button type="submit" className={styles.submitButton}>
              🎯 Confirm Booking
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

      {showModal && (
        <Modal title="🎉 Booking Confirmed!" onClose={() => setShowModal(false)}>
          <div className={styles.confirmationContent}>
            <p>✅ Your booking has been successfully confirmed!</p>
            <div className={styles.bookingDetails}>
              <p><strong>User Type:</strong> {userType}</p>
              <p><strong>Date:</strong> {date}</p>
              <p><strong>Time Slots:</strong> {selectedSlots.join(', ')}</p>
            </div>
            <p>Please arrive 5 minutes before your scheduled time.</p>
          </div>
        </Modal>
      )}
    </PageLayout>
  );
} 