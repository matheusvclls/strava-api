import axios from 'axios';
import { useEffect, useState } from 'react';
import './App.css';

function App() {

    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
  
    useEffect(() => {
      async function fetchData() {
        setIsLoading(true);
        try {
          const response = await axios.get("http://localhost:8000/activities?skip=0&limit=2", { timeout: 5000 });
          setData(response.data);
        } catch (error) {
          if(error.code === 'ECONNABORTED'){
            setError('The request took too long to complete, please try again later.')
          }
          else{
            setError(error);
          }
        } finally {
          setIsLoading(false);
        }        
      }
      fetchData();
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
  
    return <p>Data: {JSON.stringify(data)}</p>;
  }
    
export default App