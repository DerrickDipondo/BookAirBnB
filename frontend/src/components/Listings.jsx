import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';


function Listings() {
    const [listings, setListings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [bookingForm, setBookingForm] = useState({ listingId: null, date: ''});
    const { user } = useAuth();
    const navigate = useNavigate();

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

    const handleBook = (listingId) => {
        if (!user) {
            navigate('/login');
            return;
        }
        setBookingForm({ listingId, date: ''});
    }

    const handleBookingSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.post('/api/book', {
                listing_id: bookingForm.listingId,
                date: bookingForm.date,
            });
            alert(response.data.message);
            setBookingForm({ listingId: null, date: ''});
            navigate('/bookings')
        } catch (err) {
            setError(err.response?.data?.message)
        }
    };


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
                            <button onClick={() => handleBook(listing.id)} style={{ marginLeft: '10px' }}>
                                Book Now
                            </button>
                        </li>
                    ))}
                </ul>
            )}
            {bookingForm.listingId && (
                <div>
                    <h3>Book Listing</h3>
                    <form onSubmit={handleBookingSubmit}>
                        <label>
                            <button type='submit'>Confirm Booking</button>
                            <button 
                                type='button'
                                onClick={() => setBookingForm({ listingId: null, date: ''})}
                                style={{ marginLeft: '10px' }}
                                >
                                    Cancel
                            </button>
                        </label>
                    </form>
                </div>
            )}
        </div>
    );
}

export default Listings;