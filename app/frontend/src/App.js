import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegistrationPage from './components/RegistrationPage';
import LoginPage from './components/LoginPage';
import PaymentPage from './components/PaymentPage';
import SessionBookingPage from './components/SessionBookingPage';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<RegistrationPage />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/payment' element={<PaymentPage />} />
        <Route path='/booking' element={<SessionBookingPage />} />
        <Route path='/admin' element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}