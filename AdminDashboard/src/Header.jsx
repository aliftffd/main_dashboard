import React, { useState, useEffect } from 'react'
//import axios from axios // untuk dihubungkan ke api
import { MdOutlineSpeed, MdHistory, MdQuestionMark, MdTrain, MdLocationOn, MdSearch, MdFormatAlignJustify, MdOutlineNotificationsActive, MdPerson } from 'react-icons/md'
import './App.css'

function Header({ OpenSidebar }) {
  const [hasNotification, setHasNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const [showMessage, setShowMessage] = useState(false);

  useEffect(() => {
    //simulasi pengecekan data yang melebihi batas yang ditentukan
    const checkData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/check-data');
        if (response.data.dataLimitExceeded) {
          setHasNotification(true);
          setNotificationMessage('Data melebihi batas yang diizinkan!');
        } else {
          setHasNotification(false);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setHasNotification(false);
      }
    };

    checkData();
  }, []);

  const handleNotificationClick = () => {
    setShowMessage(!showMessage);
  };

  return (
    <header className='header'>
      <div className='menu-icon'>
        <MdFormatAlignJustify className='icon' onClick={OpenSidebar} />
      </div>
      <div className='header-right'>
        <div className='notification-icon' onClick={handleNotificationClick}>
          <MdOutlineNotificationsActive className='icon' />
          {hasNotification && <span className='notification-dot'></span>}
        </div>
        <MdPerson className='icon' />
      </div>
      {showMessage && hasNotification && (
        <div className='notification-message'>
          {notificationMessage}
        </div>
      )}
    </header>
  )
}

export default Header