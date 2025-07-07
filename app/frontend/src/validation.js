import validator from 'validator';
import { 
  MAX_PASSWORD_BYTES, 
  MIN_PASSWORD_LENGTH, 
  JCU_ID_LENGTH 
} from './constants';

const encoder = new TextEncoder();

export function isValidJCId(jCId) {
  return validator.isLength(jCId, { 
    min: JCU_ID_LENGTH, 
    max: JCU_ID_LENGTH 
  });
}

export function isValidPhone(phone) {
  return validator.isMobilePhone(phone);
}

export function isValidEmail(email) {
  return validator.isEmail(email);
}

export function isFittingPassword(password) {
  return encoder.encode(password).length <= MAX_PASSWORD_BYTES;
}

export function isValidPassword(password) {
  return validator.isStrongPassword(password, {
    minLength: MIN_PASSWORD_LENGTH,
    minLowercase: 1,
    minUppercase: 1,
    minNumbers: 1,
    minSymbols: 1,
  });
}

export function validateForm(member) {
  const errors = {};

  if (!member.title) errors.title = 'Required';
  if (!member.name) errors.name = 'Required';

  if (!member.jCId) {
    errors.jCId = 'Required';
  } else if  (!isValidJCId(member.jCId)) {
    errors.jCId = `ID must be exactly ${JCU_ID_LENGTH} digits`;
  }
  
  if (!member.gender) errors.gender = 'Required';
  if (!member.dateOfBirth) errors.dateOfBirth = 'Required';

  if (!member.phone) {
    errors.phone = 'Required';
  } else if (!isValidPhone(member.phone)) {
    errors.phone = 'Phone number must be valid';
  }

  if (!member.email) {
    errors.email = 'Required';
  } else if (!isValidEmail(member.email)) {
    errors.email = 'Email must be valid';
  }

  if (!member.password) {
    errors.password = 'Required';
  } else if (!isFittingPassword(member.password)) {
    errors.password = `Password must fit within ${MAX_PASSWORD_BYTES} bytes`;
  } else if (!isValidPassword(member.password)) {
    errors.password = `Password must be at least ${MIN_PASSWORD_LENGTH} characters and include` +
    ' uppercase, lowercase, digit, and special character';
  }

  if (member.emergencyContact.name || member.emergencyContact.phone) {
    if (!member.emergencyContact.name) {
      errors.emergencyContactName = 'Required with phone number';
    }
    if (!member.emergencyContact.phone) {
      errors.emergencyContactPhone = 'Required with name';
    } else if (!isValidPhone(member.emergencyContact.phone)) {
      errors.emergencyContactPhone = 'Phone number must be valid';
    }
  }

  if (member.type === 'Student' && !member.membershipTypeId) {
    errors.membershipTypeId = 'Required';
  }

  if (!member.membershipDeclared) {
    errors.membershipDeclared = 'Declaration must be accepted';
  }

  return errors;
}
