import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Listings() {
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchListings = async () => {
            try {
                const response = await axios.get('/api/listings');
                // Ensure response.data is an array
                if (Array.isArray(response.data)) {
                    setListings(response.data);
                } else {
                    console.error('Unexpected response:', response.data);
                    setError('Invalid data from server');
                    setListings([]);
                }
                setLoading(false);
            } catch (err) {
                console.error('Fetch listings error:', err.response?.data || err.message);
                setError('Failed to load listings');
                setListings([]);
                setLoading(false);
            }
        };
        fetchListings();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h2>Available Listings</h2>
            {listings.length === 0 ? (
                <p>No listings available</p>
            ) : (
                <ul>
                    {listings.map((listing) => (
                        <li key={listing.id}>
                            {listing.title} - ${listing.price} - {listing.location}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Listings;