import axios from 'axios';
import { useEffect, useState } from 'react';
import './App.css';

function App() {

  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);
      try {
        const response = await axios.get("http://localhost:8000/activities?skip=0&limit=5", { timeout: 5000 });
        setData(response.data);
      } catch (error) {
        if (error.code === 'ECONNABORTED') {
          setError('The request took too long to complete, please try again later.')
        }
        else {
          setError(error);
        }
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();

    async function getKmsRunning() {
      setIsLoading(true);
      try {
        const response = await axios.get("http://localhost:8000/metrics/total_kms_running_this_week", { timeout: 5000 });

        if (response.data > 0) {
          setMessage("You ran " + response.data.toFixed(2) + " this week")

        }
        else {

          setMessage("You did not run this week")
        }
        ;
      } catch (error) {
        if (error.code === 'ECONNABORTED') {
          setError('The request took too long to complete, please try again later.')
        }
        else {
          setError(error);
        }
      } finally {
        setIsLoading(false);
      }
    }
    getKmsRunning();

  }, []);

  if (isLoading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  if (!data) {
    return null;
  }

  return (<div className="App">
    <p>Weekly Report</p>
    <p>{message}</p>
    <p>Last 5 activities</p>
    <table>
      <thead>
        <tr>
          <th>Activity ID</th>
          <th>Distance</th>
          <th>Date</th>
          <th>Average Speed</th>
          <th>Average Heartrate</th>
        </tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.distance}</td>
            <td>{item.start_date}</td>
            <td>{item.average_speed}</td>
            <td>{item.average_heartrate}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  );
}

export default App