import { useState, useEffect } from "react";
import axios from "axios";

function Bookings() {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');


    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await.get('/api/bookings');
                if (Array.isArray(response.data)) {
                    setBookings(response.data);
                } else {
                    console.error('Unexpected response:', response.data);
                    setError('Invalid data from server');
                    setBookings([]);
                }
                setLoading(false);
            } catch (err) {
                console.error('Fetch bookings error:', err.response?.data || err.message);
                setError('Failed to load bookings');
                setBookings([]);
                setLoading(false);
            }
        };
        fetchBookings();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            <h2>My Bookings</h2>
            {bookings.length === 0 ? (
                <p>No bookings yet</p>
            ) : (
                <ul>
                    {bookings.map((booking) => (
                        <li key={booking.id}>
                            {booking.title} - ${booking.price} - {booking.location} - {booking.date}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Bookings;