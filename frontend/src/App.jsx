import axios from 'axios';
import { useEffect, useState } from 'react';
import './App.css';

function App() {

  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [messageMonth, setMessageMonth] = useState(null);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);
      try {
        const response = await axios.get("http://localhost:8000/metrics/last_five_running_actitivities", { timeout: 5000 });
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

    async function getKmsRunningMonth() {
      setIsLoading(true);
      try {
        const responseCount = await axios.get("http://localhost:8000/metrics/activities_from_current_month_count", { timeout: 5000 });
        const responseDistance = await axios.get("http://localhost:8000/metrics/activities_from_current_month", { timeout: 5000 });

        if (responseCount.data > 0) {
          setMessageMonth("You have " + responseCount.data+ " running activities. The total distance is: "+responseDistance.data.toFixed(2) + " kms.")

        }
        else {

          setMessageMonth("You did not run this week")
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
    getKmsRunningMonth();

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

  function kmhr_to_pace(kmhr) {
    var pace = 60 / kmhr;
    var minutes = Math.floor(pace);
    var seconds = Math.floor((pace - minutes) * 60);
    return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

  return (<div className="App space-y-5">

  <p class="bolded">Strava APP</p>

    <p class="bolded">Monthly Report</p>
    <p>{messageMonth}</p>
    <p class="bolded">Weekly Report</p>
    <p>{message}</p>
    <p class="bolded">Last 5 activities</p>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-blue-100 dark:text-blue-100">
        <thead class="text-xs text-neutral-900 uppercase bg-neutral-200 border-b border-neutral-400 dark:text-white">
        <tr>
          <th class="text-center">Date</th>
          <th class="text-center">Distance</th>
          <th class="text-center">Pace</th>
          <th class="text-center">Average Heartrate</th>
        </tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={item.id} class="bg-neutral-100 border-b border-neutral-200 hover:bg-neutral-300 text-neutral-900">
            <td>{item.start_date}</td>
            <td>{(item.distance/1000).toFixed(2)}</td>
            <td>{kmhr_to_pace(item.average_speed*3.6)}</td>
            <td>{item.average_heartrate}</td>
          </tr>
        ))}
      </tbody>
    </table>
    </div>
  </div>
  );
}

export default App