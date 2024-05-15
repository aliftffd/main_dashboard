import React, { useEffect, useRef, useState } from 'react';
import { MdOutlineSpeed, MdTrain, MdLocationOn } from 'react-icons/md';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import Chart from 'chart.js/auto'; // Import Chart from chart.js/auto
import GaugeComponent from 'react-gauge-component';
import io from 'socket.io-client';

const MAX_DATA_COUNT = 10;

function Home() {
  const [sensorData, setSensorData] = useState([]);
  const [socketConnected, setSocketConnected] = useState(true);
  const [gaugeValue, setGaugeValue] = useState(0);
  const chartRef = useRef(null);
  const myChart = useRef(null);

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

    socket.on('sensorData', (data) => {
      setSensorData(prevData => [...prevData, data].slice(-MAX_DATA_COUNT));
      setGaugeValue(data.speed);
    });

    return () => {
      socket.disconnect();
      if (myChart.current) {
        myChart.current.destroy();
      }
    };
  }, []);
  useEffect(() => {
    if (chartRef && chartRef.current) {
      // Check if the previous chart instance exists and destroy it
      if (myChart.current) {
        myChart.current.destroy();
      }
  
      const ctx = chartRef.current.getContext('2d');
      myChart.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: sensorData.map(d => d.date),
          datasets: [{
            label: 'Speed',
            data: sensorData.map(d => d.value),
            borderWidth: 3,
            borderColor: ['rgba(255, 99, 132, 1)'],
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text: 'Waktu'
              }
            },
            y: {
              display: true,
              title: {
                display: true,
                text: 'Kecepatan Km/jam'
              }
            }
          },
          layout: {
            padding: {
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }
          }
        },
      });
    }
  }, [sensorData]);
  
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
          <h3>300</h3>
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
      <div className='charts-wrapper'>
        <h3>Speed Chart</h3>
        <canvas ref={chartRef} width={50} height={300} />
      </div>
      <div className='gauge-chart'>
        <GaugeComponent arc={{
          subArcs: [
            {
              limit: 20,
              color: '#EA4228',
              showTick: true
            },
            {
              limit: 40,
              color: '#F58B19',
              showTick: true
            },
            {
              limit: 60,
              color: '#F5CD19',
              showTick: true
            },
            {
              limit: 100,
              color: '#5BE12C',
              showTick: true
            },
          ]
        }}
          value={gaugeValue} />
      </div>
    </main>
  )
}
export default Home;
