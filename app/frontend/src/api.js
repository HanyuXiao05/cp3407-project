import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE_URL;

export function registerMember(member) {
  return axios.post(`${API_BASE}/members`, member);
}
