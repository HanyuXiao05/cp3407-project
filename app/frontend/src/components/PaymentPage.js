import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import PageLayout from './PageLayout';
import Modal from './Modal';
import RegistrationFormField from './RegistrationFormField';
import styles from '../styles/Registration.module.css';

const PAYMENT_OPTIONS = [
  { value: 'paynow', label: 'PayNow', icon: '💳' },
  { value: 'bank', label: 'Online Banking', icon: '🏦' },
  { value: 'card', label: 'Credit/Debit Card', icon: '💳' },
];

function getPrice(type, membershipTypeId) {
  if (type === 'Student') {
    if (membershipTypeId === '1') return 50;
    if (membershipTypeId === '2') return 100;
    return 0;
  }
  if (type === 'Staff') {
    return 120;
  }
  return 0;
}

function getDescription(type, membershipTypeId) {
  if (type === 'Student') {
    if (membershipTypeId === '1') return 'Student: 50 SGD for one trimester';
    if (membershipTypeId === '2') return 'Student: 100 SGD for three trimesters';
    return '';
  }
  if (type === 'Staff') {
    return 'Staff: 120 SGD for one year (deducted by HR from salary)';
  }
  return '';
}

export default function PaymentPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { type, membershipTypeId } = location.state || {};
  const [paymentMethod, setPaymentMethod] = useState('');
  const [cardInfo, setCardInfo] = useState({ number: '', name: '', expiry: '', cvc: '' });
  const [showModal, setShowModal] = useState(false);

  const price = getPrice(type, membershipTypeId);
  const description = getDescription(type, membershipTypeId);

  const handleCardChange = (e) => {
    const { name, value } = e.target;
    setCardInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowModal(true);
  };

  const handleModalClose = () => {
    setShowModal(false);
    navigate('/session-booking');
  };

  if (!type) {
    return (
      <PageLayout title="Payment">
        <div className={styles.paymentError}>
          <div className={styles.errorCard}>
            <span className={styles.errorIcon}>⚠️</span>
            <h3>No Registration Data Found</h3>
            <p>Please complete your registration first to proceed with payment.</p>
            <button onClick={() => navigate('/')} className={styles.backButton}>
              ← Back to Registration
            </button>
          </div>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Payment">
      <div className={styles.paymentContainer}>
        <div className={styles.paymentCard}>
          <div className={styles.paymentHeader}>
            <h2>💳 Complete Your Payment</h2>
            <p>Choose your preferred payment method to complete your membership</p>
          </div>

          <div className={styles.paymentInfo}>
            <div className={styles.membershipDetails}>
              <div className={styles.membershipType}>
                <span className={styles.membershipIcon}>
                  {type === 'Student' ? '🎓' : '👨‍💼'}
                </span>
                <div>
                  <h3>{description}</h3>
                  <p className={styles.membershipSubtitle}>
                    {type === 'Student' ? 'Student Membership' : 'Staff Membership'}
                  </p>
                </div>
              </div>
              <div className={styles.priceDisplay}>
                <span className={styles.priceLabel}>Total Amount</span>
                <span className={styles.priceValue}>SGD {price}</span>
              </div>
            </div>
          </div>

          {type === 'Staff' ? (
            <div className={styles.staffPayment}>
              <div className={styles.staffInfo}>
                <span className={styles.staffIcon}>💼</span>
                <div>
                  <h3>HR Deduction</h3>
                  <p>Payment will be deducted by HR from your salary effective from the month of registration. No further action is required.</p>
                </div>
              </div>
              <button type="button" onClick={handleSubmit} className={styles.acknowledgeButton}>
                ✅ Acknowledge & Continue
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className={styles.paymentForm}>
              <div className={styles.paymentMethodSection}>
                <h3>🔄 Select Payment Method</h3>
                <div className={styles.paymentOptions}>
                  {PAYMENT_OPTIONS.map((option) => (
                    <div
                      key={option.value}
                      className={`${styles.paymentOption} ${paymentMethod === option.value ? styles.selected : ''}`}
                      onClick={() => setPaymentMethod(option.value)}
                    >
                      <input
                        type="radio"
                        id={option.value}
                        name="paymentMethod"
                        value={option.value}
                        checked={paymentMethod === option.value}
                        onChange={() => setPaymentMethod(option.value)}
                        className={styles.radioInput}
                      />
                      <label htmlFor={option.value} className={styles.paymentOptionLabel}>
                        <span className={styles.paymentIcon}>{option.icon}</span>
                        <span>{option.label}</span>
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              {paymentMethod === 'card' && (
                <div className={styles.cardDetails}>
                  <h3>💳 Card Information</h3>
                  <div className={styles.cardForm}>
                    <div className={styles.cardRow}>
                      <div className={styles.cardField}>
                        <label htmlFor="cardNumber">Card Number</label>
                        <input
                          type="text"
                          id="cardNumber"
                          name="number"
                          value={cardInfo.number}
                          onChange={handleCardChange}
                          placeholder="1234 5678 9012 3456"
                          required
                          className={styles.cardInput}
                        />
                      </div>
                      <div className={styles.cardField}>
                        <label htmlFor="cardName">Name on Card</label>
                        <input
                          type="text"
                          id="cardName"
                          name="name"
                          value={cardInfo.name}
                          onChange={handleCardChange}
                          placeholder="Cardholder Name"
                          required
                          className={styles.cardInput}
                        />
                      </div>
                    </div>
                    <div className={styles.cardRow}>
                      <div className={styles.cardField}>
                        <label htmlFor="cardExpiry">Expiry Date</label>
                        <input
                          type="text"
                          id="cardExpiry"
                          name="expiry"
                          value={cardInfo.expiry}
                          onChange={handleCardChange}
                          placeholder="MM/YY"
                          required
                          className={styles.cardInput}
                        />
                      </div>
                      <div className={styles.cardField}>
                        <label htmlFor="cardCvc">CVC</label>
                        <input
                          type="text"
                          id="cardCvc"
                          name="cvc"
                          value={cardInfo.cvc}
                          onChange={handleCardChange}
                          placeholder="CVC"
                          required
                          className={styles.cardInput}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <button type="submit" className={styles.payButton}>
                💳 Pay SGD {price}
              </button>
            </form>
          )}
        </div>

        <div className={styles.paymentInfoCard}>
          <h3>ℹ️ Payment Information</h3>
          <div className={styles.infoItems}>
            <div className={styles.infoItem}>
              <span className={styles.infoIcon}>🔒</span>
              <div>
                <h4>Secure Payment</h4>
                <p>All transactions are encrypted and secure</p>
              </div>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoIcon}>⚡</span>
              <div>
                <h4>Instant Processing</h4>
                <p>Your membership will be activated immediately</p>
              </div>
            </div>
            <div className={styles.infoItem}>
              <span className={styles.infoIcon}>📧</span>
              <div>
                <h4>Email Confirmation</h4>
                <p>You'll receive a confirmation email</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {showModal && (
        <Modal title="🎉 Payment Successful!" onClose={handleModalClose}>
          <div className={styles.successContent}>
            <div className={styles.successIcon}>✅</div>
            <p>Your payment has been processed successfully!</p>
            <div className={styles.successDetails}>
              <p><strong>Amount:</strong> SGD {price}</p>
              <p><strong>Membership:</strong> {description}</p>
            </div>
            <p>You can now proceed to book your gym sessions.</p>
          </div>
        </Modal>
      )}
    </PageLayout>
  );
} 