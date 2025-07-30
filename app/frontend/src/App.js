import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegistrationPage from './components/RegistrationPage';
import PaymentPage from './components/PaymentPage';
import SessionBookingPage from './components/SessionBookingPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<RegistrationPage />} />
        <Route path='/payment' element={<PaymentPage />} />
        <Route path='/session-booking' element={<SessionBookingPage />} />
        {/* <Route path='/booking' element={<BookingPage />} /> */}
      </Routes>
    </BrowserRouter>
  );
}