import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    const fetchListings = async () => {
      const response = await axios.get('http://localhost:5000/api/listings');
      setListings(response.data);
    };
    fetchListings();
  }, []);

  return (
    <div className='App'>
      <h1>BookAirbnb</h1>
      <ul>
        {listings.map(listing => (
          <li key={listing.id}>
            {listing.title} - ${listing.price} - {listing.location}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App
