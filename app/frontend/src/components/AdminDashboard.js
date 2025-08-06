import React, { useState, useEffect } from 'react';
import PageLayout from './PageLayout';
import styles from '../styles/AdminDashboard.module.css';
import membersCSV from '../data/MEMBER.csv';
import bookingsCSV from '../data/BOOKING.csv';
import sessionsCSV from '../data/SESSION.csv';
import membershipCSV from '../data/MEMBERSHIP.csv';
import Papa from 'papaparse';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function AdminDashboard() {
  const [members, setMembers] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  // const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedDate, setSelectedDate] = useState('2025-09-26');
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data for demo purposes
  // const mockMembers = [
  //   {
  //     member_id: 'M001',
  //     name: 'Tyler Pope',
  //     email: 'tyler.pope@student.jcu.edu.au',
  //     membership_type: 'Student',
  //     join_date: '2024-01-15',
  //     status: 'Active',
  //     total_bookings: 12,
  //     last_booking: '2025-09-30'
  //   },
  //   {
  //     member_id: 'M002',
  //     name: 'Erika Bowen',
  //     email: 'erika.bowen@student.jcu.edu.au',
  //     membership_type: 'Student',
  //     join_date: '2024-02-20',
  //     status: 'Active',
  //     total_bookings: 8,
  //     last_booking: '2025-09-29'
  //   },
  //   {
  //     member_id: 'M003',
  //     name: 'Vera Alvarado',
  //     email: 'vera.alvarado@student.jcu.edu.au',
  //     membership_type: 'Student',
  //     join_date: '2024-03-10',
  //     status: 'Active',
  //     total_bookings: 15,
  //     last_booking: '2025-09-30'
  //   },
  //   {
  //     member_id: 'M004',
  //     name: 'Aria Williams',
  //     email: 'aria.williams@student.jcu.edu.au',
  //     membership_type: 'Student',
  //     join_date: '2024-01-05',
  //     status: 'Active',
  //     total_bookings: 6,
  //     last_booking: '2025-09-28'
  //   },
  //   {
  //     member_id: 'M005',
  //     name: 'Ella Brown',
  //     email: 'ella.brown@student.jcu.edu.au',
  //     membership_type: 'Student',
  //     join_date: '2024-02-15',
  //     status: 'Active',
  //     total_bookings: 10,
  //     last_booking: '2025-09-30'
  //   }
  // ];

  // const mockBookings = [
  //   {
  //     booking_ref: 'BK20250930080001',
  //     member_id: 'M001',
  //     member_name: 'Tyler Pope',
  //     date: '2025-09-30',
  //     time: '08:00 - 09:00',
  //     status: 'Booked',
  //     check_in: null,
  //     check_out: null
  //   },
  //   {
  //     booking_ref: 'BK20250930090001',
  //     member_id: 'M001',
  //     member_name: 'Tyler Pope',
  //     date: '2025-09-30',
  //     time: '09:00 - 10:00',
  //     status: 'Booked',
  //     check_in: null,
  //     check_out: null
  //   },
  //   {
  //     booking_ref: 'BK20250930080002',
  //     member_id: 'M003',
  //     member_name: 'Vera Alvarado',
  //     date: '2025-09-30',
  //     time: '08:00 - 09:00',
  //     status: 'Attended',
  //     check_in: '2025-09-30 08:02',
  //     check_out: '2025-09-30 08:50'
  //   },
  //   {
  //     booking_ref: 'BK20250930090002',
  //     member_id: 'M005',
  //     member_name: 'Ella Brown',
  //     date: '2025-09-30',
  //     time: '09:00 - 10:00',
  //     status: 'No-Show',
  //     check_in: null,
  //     check_out: null
  //   }
  // ];

  // useEffect(() => {
  //   setMembers(mockMembers);
  //   setBookings(mockBookings);
  // }, []);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(membersCSV)
        .then(r => r.text())
        .then(txt => Papa.parse(txt, { header: true, dynamicTyping: true }).data),
      fetch(bookingsCSV)
        .then(r => r.text())
        .then(txt => Papa.parse(txt, { header: true, dynamicTyping: true }).data),
      fetch(sessionsCSV)
        .then(r => r.text())
        .then(txt => Papa.parse(txt, { header: true, dynamicTyping: true }).data),
      fetch(membershipCSV)
        .then(r => r.text())
        .then(txt => Papa.parse(txt, { header: true, dynamicTyping: true }).data),
    ])
      .then(([membersData, rawBookings, sessionsData, membershipData]) => {
        setMembers(membersData);

        const startDate = '2025-09-26';
        const endDate = '2025-10-02';

        const filteredBookings = rawBookings
          .map((bk) => {
            const session = sessionsData.find((s) => s.SESSION_ID === bk.SESSION_ID);
            if (!session) return null;

            const date = session.SESSION_Date;
            if (date < startDate || date > endDate) return null;

            const [h, m] = session.SESSION_Time.split(':');
            const endHour = String((Number(h) + 1));
            const time = `${session.SESSION_Time.slice(0,5)} - ${endHour}:${m}`;
            
            const member = membersData.find((m) => m.MEMBER_ID === bk.MEMBER_ID);

            return {
              booking_ref: bk.BOOKING_Ref,
              member_id: bk.MEMBER_ID,
              member_name: member ? member.MEMBER_Name : '',
              status: bk.BOOKING_Status,
              date,
              time,
              check_in: null,
              check_out: null,
            };
          })
          .filter(Boolean);

        const membersWithStats = membersData.map(mem => {
          const memberId = mem.MEMBER_ID;
          const membership = membershipData.find(m => m.MEMBER_ID === memberId);
          const joinDate = membership ? membership.MEMBERSHIP_StartDate : '';
          const expDate  = membership ? membership.MEMBERSHIP_ExpDate   : '';
          const status   = expDate >= selectedDate ? 'Active' : 'Expired';
          const memberBookings = filteredBookings.filter(b => String(b.member_id) === String(memberId));
          const totalBookings = memberBookings.length;
          const lastBooking   = totalBookings > 0
            ? memberBookings.map(b => b.date).sort().pop()
            : '';

          return {
            member_id: mem.MEMBER_ID,
            name:      mem.MEMBER_Name,
            email:     mem.MEMBER_Email,
            membership_type: mem.MEMBER_Type,
            join_date: joinDate,
            status,
            total_bookings: totalBookings,
            last_booking:   lastBooking,
          };
        });

        const bookingsWithNames = filteredBookings.map(bk => {
          const member = membersWithStats.find(m => m.member_id === bk.member_id);
          return {
            ...bk,
            member_name: member?.name || '',
            check_in:    bk.BOOKING_CheckIn  || null,
            check_out:   bk.BOOKING_CheckOut || null,
          };
        });        

        setMembers(membersWithStats);
        setBookings(bookingsWithNames);
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to load mock data.');
      })
      .finally(() => setLoading(false));
  }, [selectedDate]);

  const getWeeklyData = () => {
    const startOfWeek = new Date(selectedDate);
    const day = startOfWeek.getDay();
    const diffToMonday = ((day + 6) % 7);
    startOfWeek.setDate(startOfWeek.getDate() - diffToMonday);
    const weekData = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(startOfWeek);
      d.setDate(startOfWeek.getDate() + i);
      const dateString = d.toISOString().split('T')[0];
      const count = bookings.filter(b => b.date === dateString).length;
      weekData.push({ day: d.toLocaleDateString('en-US', { weekday: 'short' }), count });
    }
    return weekData;
  };

  const getHourlyData = () => {
    const hours = [];
    for (let h = 6; h <= 22; h++) {
      const label = `${h}:00`;
      const used = bookings.filter(b => b.date === selectedDate && Number(b.time.split(':')[0]) === h).length;
      hours.push({ hour: label, used });
    }
    return hours;
  };

  const weeklyData = getWeeklyData();
  const hourlyData = getHourlyData();

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active': return '#28a745';
      case 'Booked': return '#007bff';
      case 'Attended': return '#28a745';
      case 'No-Show': return '#dc3545';
      case 'Cancelled': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const getTodayStats = () => {
    const todayBookings = bookings.filter(b => b.date === selectedDate);
    const totalBookings = todayBookings.length;
    const attendedBookings = todayBookings.filter(b => b.status === 'Attended').length;
    const noShowBookings = todayBookings.filter(b => b.status === 'No-Show').length;
    const activeBookings = todayBookings.filter(b => b.status === 'Booked').length;

    return {
      total: totalBookings,
      attended: attendedBookings,
      noShow: noShowBookings,
      active: activeBookings
    };
  };

  const stats = getTodayStats();

  if (loading) {
    return (
      <PageLayout>
        <p>Loading mock data...</p>
      </PageLayout>
    );
  }
  if (error) {
    return (
      <PageLayout>
        <p>Error: {error}</p>
      </PageLayout>
    );
  }

  return (
    <PageLayout>
      <div className={styles.adminContainer}>
        <div className={styles.header}>
          <h1>👨‍💼 Admin Dashboard</h1>
          <p>Monitor gym members, reservations, and attendance</p>
        </div>

        <div className={styles.tabNavigation}>
          <button 
            className={`${styles.tabButton} ${activeTab === 'overview' ? styles.active : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            📊 Overview
          </button>
          <button 
            className={`${styles.tabButton} ${activeTab === 'members' ? styles.active : ''}`}
            onClick={() => setActiveTab('members')}
          >
            👥 Members
          </button>
          <button 
            className={`${styles.tabButton} ${activeTab === 'bookings' ? styles.active : ''}`}
            onClick={() => setActiveTab('bookings')}
          >
            📅 Bookings
          </button>
          <button 
            className={`${styles.tabButton} ${activeTab === 'attendance' ? styles.active : ''}`}
            onClick={() => setActiveTab('attendance')}
          >
            ✅ Attendance
          </button>
        </div>

        {activeTab === 'overview' && (
          <div className={styles.overviewTab}>
            <div className={styles.dateSelector}>
              <label htmlFor="date">Select Date:</label>
              <input
                type="date"
                id="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className={styles.dateInput}
              />
            </div>

            <div className={styles.statsGrid}>
              <div className={styles.statCard}>
                <h3>Total Bookings</h3>
                <div className={styles.statValue}>{stats.total}</div>
                <div className={styles.statLabel}>Today's reservations</div>
              </div>
              <div className={styles.statCard}>
                <h3>Attended</h3>
                <div className={styles.statValue} style={{color: '#28a745'}}>{stats.attended}</div>
                <div className={styles.statLabel}>Successful sessions</div>
              </div>
              <div className={styles.statCard}>
                <h3>No-Show</h3>
                <div className={styles.statValue} style={{color: '#dc3545'}}>{stats.noShow}</div>
                <div className={styles.statLabel}>Missed sessions</div>
              </div>
              <div className={styles.statCard}>
                <h3>Active</h3>
                <div className={styles.statValue} style={{color: '#007bff'}}>{stats.active}</div>
                <div className={styles.statLabel}>Upcoming sessions</div>
              </div>
              <div className={styles.chartCard}>
                <h3>Gym Usage This Week</h3>
                <ResponsiveContainer width="100%" height={150}>
                  <BarChart data={weeklyData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#007bff" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className={styles.chartCard}>
                <h3>Gym Usage Today</h3>
                <ResponsiveContainer width="100%" height={150}>
                  <BarChart data={hourlyData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
                    <XAxis dataKey="hour" tick={{ fontSize: 10 }} />
                    <YAxis domain={[0, 6]} />
                    <Tooltip />
                    <Bar dataKey="used" fill="#007bff" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className={styles.recentActivity}>
              <h3>📈 Recent Activity</h3>
              <div className={styles.activityList}>
                {bookings.slice(0, 5).map((booking, index) => (
                  <div key={index} className={styles.activityItem}>
                    <div className={styles.activityInfo}>
                      <span className={styles.memberName}>{booking.member_name}</span>
                      <span className={styles.bookingTime}>{booking.date} at {booking.time}</span>
                    </div>
                                         <span 
                       className={styles.statusBadge}
                       style={{backgroundColor: getStatusColor(booking.status)}}>
                       {booking.status}
                     </span>
                   </div>
                 ))}
               </div>
             </div>
           </div>
         )}

        {activeTab === 'members' && (
          <div className={styles.membersTab}>
            <div className={styles.tableHeader}>
              <h3>👥 Member Information</h3>
              <div className={styles.searchBox}>
                <input 
                  type="text" 
                  placeholder="Search members..."
                  className={styles.searchInput}
                />
              </div>
            </div>
            
            <div className={styles.membersTable}>
              <table>
                <thead>
                  <tr>
                    <th>Member ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Membership</th>
                    <th>Join Date</th>
                    <th>Status</th>
                    <th>Total Bookings</th>
                    <th>Last Booking</th>
                  </tr>
                </thead>
                <tbody>
                  {members.map((member) => (
                    <tr key={member.member_id}>
                      <td>{member.member_id}</td>
                      <td>{member.name}</td>
                      <td>{member.email}</td>
                      <td>{member.membership_type}</td>
                      <td>{member.join_date}</td>
                      <td>
                        <span 
                          className={styles.statusBadge}
                          style={{backgroundColor: getStatusColor(member.status)}}>
                          {member.status}
                        </span>
                      </td>
                      <td>{member.total_bookings}</td>
                      <td>{member.last_booking}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'bookings' && (
          <div className={styles.bookingsTab}>
            <div className={styles.tableHeader}>
              <h3>📅 Booking Management</h3>
              <div className={styles.filterControls}>
                <select className={styles.filterSelect}>
                  <option value="">All Status</option>
                  <option value="Booked">Booked</option>
                  <option value="Attended">Attended</option>
                  <option value="No-Show">No-Show</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className={styles.dateInput}
                />
              </div>
            </div>

            <div className={styles.bookingsTable}>
              <table>
                <thead>
                  <tr>
                    <th>Booking Ref</th>
                    <th>Member</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Check In</th>
                    <th>Check Out</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings.map((booking) => (
                    <tr key={booking.booking_ref}>
                      <td>{booking.booking_ref}</td>
                      <td>{booking.member_name}</td>
                      <td>{booking.date}</td>
                      <td>{booking.time}</td>
                      <td>
                        <span 
                          className={styles.statusBadge}
                          style={{backgroundColor: getStatusColor(booking.status)}}>
                          {booking.status}
                        </span>
                      </td>
                      <td>{booking.check_in || '-'}</td>
                      <td>{booking.check_out || '-'}</td>
                      <td>
                        <div className={styles.actionButtons}>
                          <button className={styles.actionBtn}>Edit</button>
                          <button className={styles.actionBtn}>Cancel</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'attendance' && (
          <div className={styles.attendanceTab}>
            <h3>✅ Attendance Tracking</h3>
            <span className={styles.attRate}>
              Today's Attendance Rate:{" "}
              {stats.attended && stats.total
                ? Math.round((stats.attended / stats.total) * 100)
                : 0}
              %
            </span>
            <div className={styles.attendanceTable}>
              <table>
                <thead>
                  <tr>
                    <th>Member</th>
                    <th>Time</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings
                    .filter(b => b.date === selectedDate)
                    .map(b => (
                      <tr key={b.booking_ref}>
                        <td>{b.member_name}</td>
                        <td>{b.time}</td>
                        <td>
                          <span
                            className={styles.statusBadge}
                            style={{ backgroundColor: getStatusColor(b.status) }}
                          >
                            {b.status}
                          </span>
                        </td>
                      </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </PageLayout>
  );
} 