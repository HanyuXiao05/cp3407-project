import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import PageLayout from './PageLayout';
import Modal from './Modal';
import styles from '../styles/Payment.module.css';

export default function PaymentPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [paymentData, setPaymentData] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    cardholderName: '',
    paymentType: 'credit_card',
    bankTransferDetails: '',
    netsDetails: ''
  });
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Get member data from registration (if available)
  const memberData = location.state?.memberData || {};

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPaymentData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validatePaymentForm = () => {
    const errors = {};
    
    if (paymentData.paymentType === 'credit_card' || paymentData.paymentType === 'debit_card') {
      if (!paymentData.cardNumber || paymentData.cardNumber.length < 16) {
        errors.cardNumber = 'Please enter a valid card number';
      }
      
      if (!paymentData.expiryDate) {
        errors.expiryDate = 'Please enter expiry date';
      }
      
      if (!paymentData.cvv || paymentData.cvv.length < 3) {
        errors.cvv = 'Please enter a valid CVV';
      }
      
      if (!paymentData.cardholderName) {
        errors.cardholderName = 'Please enter cardholder name';
      }
    } else if (paymentData.paymentType === 'bank_transfer') {
      if (!paymentData.bankTransferDetails) {
        errors.bankTransferDetails = 'Please provide bank transfer details';
      }
    } else if (paymentData.paymentType === 'nets') {
      if (!paymentData.netsDetails) {
        errors.netsDetails = 'Please provide your NETS details';
      }
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    const errors = validatePaymentForm();
    if (Object.keys(errors).length > 0) {
      setError('Please fill in all required fields correctly');
      return;
    }

    setLoading(true);
    
    try {
      // Mock payment processing - in real app, this would call the payment API
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setShowModal(true);
      setLoading(false);
    } catch (error) {
      setError('Payment failed. Please try again.');
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    navigate('/booking', { state: { memberData } });
  };

  return (
    <>
      <PageLayout title="PAYMENT DETAILS">
        <div className={styles.paymentContainer}>
          <div className={styles.paymentInfo}>
            <h3>Membership Fee: $50.00</h3>
            <p>Please complete your payment to activate your gym membership.</p>
          </div>

          <form onSubmit={handleSubmit} className={styles.paymentForm}>
            <div className={styles.formGroup}>
              <label htmlFor="paymentType">Payment Method</label>
              <select
                id="paymentType"
                name="paymentType"
                value={paymentData.paymentType}
                onChange={handleInputChange}
                className={styles.paymentSelect}
              >
                <option value="credit_card">💳 Credit Card</option>
                <option value="debit_card">💳 Debit Card</option>
                <option value="nets">NETS</option>
                <option value="bank_transfer">🏦 Bank Transfer</option>
                <option value="cash">💵 Cash Payment</option>
              </select>
            </div>

            {/* Credit/Debit Card Fields - Only show if selected */}
            {(paymentData.paymentType === 'credit_card' || paymentData.paymentType === 'debit_card') && (
              <>
                <div className={styles.formGroup}>
                  <label htmlFor="cardholderName">Cardholder Name</label>
                  <input
                    type="text"
                    id="cardholderName"
                    name="cardholderName"
                    value={paymentData.cardholderName}
                    onChange={handleInputChange}
                    placeholder="Enter cardholder name"
                  />
                </div>

                <div className={styles.formGroup}>
                  <label htmlFor="cardNumber">Card Number</label>
                  <input
                    type="text"
                    id="cardNumber"
                    name="cardNumber"
                    value={paymentData.cardNumber}
                    onChange={handleInputChange}
                    placeholder="1234 5678 9012 3456"
                    maxLength="19"
                  />
                </div>

                <div className={styles.formRow}>
                  <div className={styles.formGroup}>
                    <label htmlFor="expiryDate">Expiry Date</label>
                    <input
                      type="text"
                      id="expiryDate"
                      name="expiryDate"
                      value={paymentData.expiryDate}
                      onChange={handleInputChange}
                      placeholder="MM/YY"
                      maxLength="5"
                    />
                  </div>

                  <div className={styles.formGroup}>
                    <label htmlFor="cvv">CVV</label>
                    <input
                      type="text"
                      id="cvv"
                      name="cvv"
                      value={paymentData.cvv}
                      onChange={handleInputChange}
                      placeholder="123"
                      maxLength="4"
                    />
                  </div>
                </div>
              </>
            )}

            {/* NETS Fields - Only show if selected */}
            {paymentData.paymentType === 'nets' && (
              <div className={styles.formGroup}>
                <label htmlFor="netsDetails">NETS Payment Details</label>
                <div className={styles.netsInfo}>
                  <p>Please provide your NETS payment information:</p>
                  <ul>
                    <li>NETS FlashPay card number</li>
                    <li>Or NETS bank account details</li>
                    <li>Or NETS QR code payment</li>
                  </ul>
                </div>
                <textarea
                  id="netsDetails"
                  name="netsDetails"
                  value={paymentData.netsDetails}
                  onChange={handleInputChange}
                  placeholder="Enter your NETS payment details (card number, bank account, or QR code info)"
                  rows="4"
                  className={styles.textarea}
                />
              </div>
            )}

            {/* Bank Transfer Fields - Only show if selected */}
            {paymentData.paymentType === 'bank_transfer' && (
              <div className={styles.formGroup}>
                <label htmlFor="bankTransferDetails">Bank Transfer Details</label>
                <textarea
                  id="bankTransferDetails"
                  name="bankTransferDetails"
                  value={paymentData.bankTransferDetails}
                  onChange={handleInputChange}
                  placeholder="Please provide your bank account details for transfer"
                  rows="4"
                  className={styles.textarea}
                />
              </div>
            )}

            {/* Cash Payment Info - Only show if selected */}
            {paymentData.paymentType === 'cash' && (
              <div className={styles.cashInfo}>
                <h4>💵 Cash Payment Instructions</h4>
                <div className={styles.memberTypeSection}>
                  <h5>New Members:</h5>
                  <p>To become a member, please visit the Campus Activities office with a valid JCU Student ID during office hours. The trained staff member will do an induction of the gym handbook. Once the member has fully understood and agreed to abide by terms and conditions, payment will be completed.</p>
                </div>
                <div className={styles.memberTypeSection}>
                  <h5>Renewing Members:</h5>
                  <p>Members who are renewing their expired membership can renew at Campus Activities, and payment will be completed during the renewal process.</p>
                </div>
                <div className={styles.paymentDetails}>
                  <h5>Payment Details:</h5>
                  <ul>
                    <li>Payment amount: $50.00</li>
                    <li>Bring your registration confirmation</li>
                    <li>Valid JCU Student ID required</li>
                  </ul>
                </div>
              </div>
            )}

            {error && <div className={styles.error}>{error}</div>}

            <div className={styles.buttonGroup}>
              <button
                type="button"
                onClick={() => navigate('/')}
                className={styles.secondaryButton}
              >
                Back to Registration
              </button>
              <button
                type="submit"
                disabled={loading}
                className={styles.primaryButton}
              >
                {loading ? 'Processing...' : 'Pay $50.00'}
              </button>
            </div>
          </form>
        </div>
      </PageLayout>

      {showModal && (
        <Modal onClose={handleCloseModal}>
          <div className={styles.successMessage}>
            <h3>Payment Successful!</h3>
            <p>Your gym membership has been activated.</p>
            <p>You can now proceed to book your gym sessions.</p>
            <button onClick={handleCloseModal} className={styles.primaryButton}>
              Continue to Session Booking
            </button>
          </div>
        </Modal>
      )}
    </>
  );
} 