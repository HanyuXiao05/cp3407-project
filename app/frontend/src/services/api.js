import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

export function registerMember(member) {
  return axios.post(`${API_BASE}/auth/register`, member);
}

export function loginMember(credentials) {
  return axios.post(`${API_BASE}/auth/login`, credentials);
}
