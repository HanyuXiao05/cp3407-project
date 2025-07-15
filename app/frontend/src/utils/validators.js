import validator from 'validator';
import {
  JCU_ID_LENGTH,
  MAX_PASSWORD_BYTES, 
  MIN_PASSWORD_LENGTH  
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