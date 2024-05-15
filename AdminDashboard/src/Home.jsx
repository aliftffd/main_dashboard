import React, { useEffect, useRef, useState } from 'react';
import { MdOutlineSpeed, MdTrain, MdLocationOn } from 'react-icons/md';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'; // Import Legend from recharts
import GaugeComponent from 'react-gauge-component';
import io from 'socket.io-client';

const MAX_DATA_COUNT = 10;
const MAX_SPEED = 100;

const gaugeLimits = [
  { limit: 20, color: '#EA4228', showTick: true },
  { limit: 40, color: '#F58B19', showTick: true },
  { limit: 60, color: '#F5CD19', showTick: true },
  { limit: MAX_SPEED, color: '#5BE12C', showTick: true },
];

function Home() {
  const [sensorData, setSensorData] = useState([]);
  const [socketConnected, setSocketConnected] = useState([]);
  const [gaugeValue, setGaugeValue] = useState(0);
  const chartRef = useRef(null);
  const myChart = useRef(null);

  const gaugeValueInPercentage = (gaugeValue) => {
    return (gaugeValue / MAX_SPEED) * 100;
  };

  useEffect(() => {
    const URL = "http://localhost:5001";
    const socket = io(URL, {
      pinTimeout : 30000,
      pingInterval : 5000,
      upgradeTimeout : 30000, 
      cors : { 
        origin : "http://localhost:5001",
      }
    });
    socket.connect();
    console.log(socket)
    
    socket.on("connect_error", (err) => {
      console.log(`connect_error due to ${err.message}`);
    });

    socket.on('connect', () => {
      setSocketConnected(true);
    });

    socket.on('disconnect', () => {
      setSocketConnected(false);
    });

    socket.on('sensorData', ({ value }) => {
      console.log(value); // Destructure the 'value' from the data object
      setSensorData(prevData => [...prevData, { value }].slice(-MAX_DATA_COUNT));
      setGaugeValue(value); // Set the gauge value directly from the 'value' property
    
      const speedValueElement = document.getElementById('speedValue');
      if (speedValueElement) {
        speedValueElement.innerText = value; // Update the speed value in the DOM if the element exists
      }
    });
    
    return () => {
      socket.disconnect();
      if (myChart.current) {
        myChart.current.destroy();
      }
    };
  }, []);
  
  return (
    <main className='main-container'>
      <div className='main-title'>
        <h1>DASHBOARD</h1>
      </div>
      <div className='main-cards'>
        <div className='card'>
          <div className='card-inner'>
            <h3>Speed Rated</h3>
            <MdOutlineSpeed className='card_icon' />
          </div>
          <h3 id='speedValue'>{sensorData.length > 0 ? sensorData[sensorData.length - 1].value : 0}</h3>
        </div>
        <div className='card'>
          <div className='card-inner'>
            <h3>Train Position</h3>
            <MdTrain className='card_icon' />
          </div>
          <h3>33</h3>
        </div>
        <div className='card'>
          <div className='card-inner'>
            <h3>Blocking</h3>
            <MdLocationOn className='card_icon' />
          </div>
          <h3>42</h3>
        </div>
      </div>
      <div className='charts-wrapper' style={{ display: 'flex', justifyContent: 'space-between' }}> {/* Add a style to display the charts side by side */}
      <div className='line-chart' style={{ flex: 1 }}> {/* Add a style to make the chart take up half the space */}
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            width={500}
            height={300}
            data={sensorData.map(({ value, ...rest }) => ({ ...rest, speed: value }))}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="speed" stroke="#8884d8" activeDot={{ r: 8 }} /> {/* Change 'value' to 'speed' */}
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className='gauge-chart' style={{ flex: 1, maxWidth: '500px' }}> {/* Add a style to make the chart take up half the space */}
        <GaugeComponent 
        arc={{ subArcs: gaugeLimits }}
        value={gaugeValueInPercentage(gaugeValue)} />
      </div>
    </div>
  </main>
  )
}
export default Home;
