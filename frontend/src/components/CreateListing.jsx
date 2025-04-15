import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function CreateListing() {
    const [title, setTitle] = useState('');
    const [price, setPrice] = useState('');
    const [location, setLocation] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        const payload = {
            title,
            price: parseFloat(price),
            location,
        };
        console.log('Sending payload:', payload);
        try {
            const response = await axios.post('/api/listings', payload);
            console.log('Response:', response.data);
            setSuccess(response.data.message);
            setTitle('');
            setPrice('');
            setLocation('');
            setTimeout(() => navigate('/'), 2000);
        } catch (err) {
            console.error('Create listing error:', err.response?.data || err.message);
            setError(err.response?.data?.message || 'Failed to create listing');
        }
    };

    return (
        <div>
            <h2>Create a New Listing</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Price per Night ($):</label>
                    <input
                        type="number"
                        step="0.01"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Location:</label>
                    <input
                        type="text"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Create Listing</button>
            </form>
        </div>
    );
}

export default CreateListing;