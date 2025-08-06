export const JCU_ID_LENGTH =  8;
export const MAX_PASSWORD_BYTES = 72;
export const MIN_PASSWORD_LENGTH = 8;

export const EMPTY_MEMBER = {
  type: '',
  title: '',
  name: '',
  jCId: '',
  gender: '',
  dateOfBirth: '',
  phone: '',
  email: '',
  password: '',
  emergencyContact: {
    name: '',
    phone: '',
  },
  membershipTypeId: '',
  membershipDeclared: false
};