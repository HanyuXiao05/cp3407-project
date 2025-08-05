import styles from '../styles/Registration.module.css';
import { useState } from 'react';
import { EMPTY_MEMBER } from '../utils/constants';
import { useNavigate } from 'react-router-dom';
import { validateRegistrationForm } from '../utils/validateRegistrationForm';
// import { registerMember } from '../services/api';
import RegistrationFormField from './RegistrationFormField';
import Modal from './Modal';

export default function RegistrationForm() {
  const [member, setMember] = useState(EMPTY_MEMBER);
  const navigate = useNavigate();

  const [errorMessages, setErrorMessages] = useState({});
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    const errors = validateRegistrationForm(member);
    setErrorMessages(errors);
    if (Object.keys(errors).length > 0) return;
  
    // registerMember(member)
    //   .then((response) => {
    //     console.log('Submitted:', response.data);

        // alert('Registration successful!');
        setShowModal(true);

        setMember(EMPTY_MEMBER);
        
        setErrorMessages({});
      // })
      // .catch((error) => {
      //   console.error('Error:', error);
      // });
  };

  const handleClose = () => {
    setShowModal(false);
    navigate('/payment', { state: { memberData: member } });
  };

  return (
    <>
      <form  onSubmit={handleSubmit} className={styles.formGrid} noValidate>
        <RegistrationFormField
          fieldArea ={styles.leftColumn}
          label='Member Type'
          htmlFor='type'
        >
          <select
            name='type'
            id='type'
            value={member.type}
            onChange={(e) => setMember((prev) => ({ ...prev, type: e.target.value }))}
          >
            <option value=''>-- Select Member Type --</option>
            <option value='Staff'>Staff</option>
            <option value='Student'>Student</option>
          </select>
        </RegistrationFormField>

        {member.type && (
          <>
            <RegistrationFormField
              fieldArea ={styles.leftColumn}
              label='Title'
              htmlFor='title'
              error={errorMessages.title}
            >
              <select
                name='title'
                id='title'
                value={member.title}
                onChange={(e) => setMember((prev) => ({ ...prev, title: e.target.value }))}
              >
                <option value=''>-- Select Title --</option>
                <option value='Mr'>Mr</option>
                <option value='Mrs'>Mrs</option>
                <option value='Ms'>Ms</option>
              </select>
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.rightColumn}
              label='Full Name'
              htmlFor='name'
              error={errorMessages.name}
            >
              <input
                type='text'
                name='name'
                id='name'
                value={member.name}
                onChange={(e) => setMember((prev) => ({ ...prev, name: e.target.value }))}
                placeholder='Full Name'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.leftColumn}
              label='JCU ID'
              htmlFor='jCId'
              error={errorMessages.jCId}
            >
              <input
                type='number'
                name='jCId'
                id='jCId'
                value={member.jCId}
                onChange={(e) => setMember((prev) => ({ ...prev, jCId: e.target.value }))}
                placeholder='JCU ID'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.rightColumn}
              label='Gender'
              htmlFor='gender'
              error={errorMessages.gender}
            >
              <select
                name='gender'
                id='gender'
                value={member.gender}
                onChange={(e) => setMember((prev) => ({ ...prev, gender: e.target.value }))}
              >
                <option value=''>-- Select Gender --</option>
                <option value='Male'>Male</option>
                <option value='Female'>Female</option>
              </select>
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.leftColumn}
              label='Date of Birth'
              htmlFor='dateOfBirth'
              error={errorMessages.dateOfBirth}
            >
              <input
                type='date'
                name='dateOfBirth'
                id='dateOfBirth'
                value={member.dateOfBirth}
                onChange={(e) => setMember((prev) => ({ ...prev, dateOfBirth: e.target.value }))}
              />
            </RegistrationFormField>
            
            <RegistrationFormField
              fieldArea ={styles.rightColumn}
              label='Mobile Number'
              htmlFor='phone'
              error={errorMessages.phone}
            >
              <input
                type='tel'
                name='phone'
                id='phone'
                value={member.phone}
                onChange={(e) => setMember((prev) => ({ ...prev, phone: e.target.value }))}
                placeholder='Phone Number'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.leftColumn}
              label='Email'
              htmlFor='email'
              error={errorMessages.email}
            >
              <input
                type='email'
                name='email'
                id='email'
                value={member.email}
                onChange={(e) => setMember((prev) => ({ ...prev, email: e.target.value }))}
                placeholder='Email Address'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.rightColumn}
              label='Password'
              htmlFor='password'
              error={errorMessages.password}
            >
              <input
                type='password'
                name='password'
                id='password'
                value={member.password}
                onChange={(e) => setMember((prev) => ({ ...prev, password: e.target.value }))}
                placeholder='Password'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.leftColumn}
              label='Emergency Contact Name'
              htmlFor='emergencyContactName'
              error={errorMessages.emergencyContactName}
            >
              <input
                type='text'
                name='emergencyContactName'
                id='emergencyContactName'
                value={member.emergencyContact.name}
                onChange={(e) =>
                  setMember((prev) => ({
                  ...prev,
                  emergencyContact: {
                      ...prev.emergencyContact,
                      name: e.target.value,
                  },
                  }))
                }
                placeholder='Full Name'
              />
            </RegistrationFormField>

            <RegistrationFormField
              fieldArea ={styles.rightColumn}
              label='Emergency Contact Phone'
              htmlFor='emergencyContactPhone'
              error={errorMessages.emergencyContactPhone}
            >
              <input
                type='tel'
                name='emergencyContactPhone'
                id='emergencyContactPhone'
                value={member.emergencyContact.phone}
                onChange={(e) =>
                  setMember((prev) => ({
                  ...prev,
                  emergencyContact: {
                      ...prev.emergencyContact,
                      phone: e.target.value,
                  },
                  }))
                }
                placeholder='Phone Number'
              />
            </RegistrationFormField>

            {member.type === 'Student' && (
              <>
                <RegistrationFormField
                  fieldArea ={styles.leftColumn}
                  label='Membership Type'
                  htmlFor='membershipTypeId'
                  error={errorMessages.membershipTypeId}
                >
                  <select
                    name='membershipTypeId'
                    id='membershipTypeId'
                    value={member.membershipTypeId}
                    onChange={(e) => setMember((prev) => 
                      ({ ...prev, membershipTypeId: e.target.value }))}
                  >
                    <option value=''>-- Select Membership Type --</option>
                    <option value='1'>One Trimester</option>
                    <option value='2'>Three Trimesters</option>
                  </select>
                </RegistrationFormField>
              </>
            )}

            <RegistrationFormField
              fieldArea ={styles.declarationRow}
              htmlFor='membershipDeclared'
              error={errorMessages.membershipDeclared}
            >
              <input
                type='checkbox'
                name='membershipDeclared'
                id='membershipDeclared'
                checked={member.membershipDeclared}
                onChange={(e) => 
                  setMember((prev) => ({...prev, membershipDeclared: e.target.checked}))}
              />
              <label htmlFor='membershipDeclared'>
                I have read and agree to the terms and conditions contained in the <a 
                href='https://www.jcu.edu.sg/privacy' target='_blank' 
                rel='noopener noreferrer'>Privacy Policy of Singapore campus of James 
                Cook University</a>. I have read, understood and hereby agree to the 
                terms and conditions of membership as set out in the <a 
                href='/policies-and-procedures.html' target='_blank' 
                rel='noopener noreferrer'>Policies and Procedures</a> attached to this 
                Membership and Indemnity form and I am fully aware that it affects my 
                legal rights. 
              </label>
            </RegistrationFormField>

            <div className={styles.registrationRow}>
              <button type='submit'>Register</button>
            </div>
          </>
        )}
      </form>

      {showModal && (
        <Modal
          title='MEMBERSHIP ACTIVATED'
          onClose={handleClose}
        >
          <p>
            An email has been sent to your registered email address containing your membership 
            and payment details, along with the Gym Handbook.
          </p>
          <p>
            If you have not received it, please check your spam/junk mail or verify that your 
            details are correct.
          </p>
        </Modal>
      )}
    </>
  );
}