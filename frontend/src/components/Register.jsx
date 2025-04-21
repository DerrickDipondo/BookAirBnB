import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isHost, setIsHost] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        console.log('Register payload:', { email, password, is_host: isHost });
        try {
            const response = await axios.post('/api/register', { email, password, is_host: isHost });
            console.log('Register response:', response.data);
            navigate('/login');
        } catch (err) {
            console.error('Register error:', err.response?.data || err.message);
            setError(err.response?.data?.message || 'Registration failed');
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                </div>
                <label>
                    <input
                        type="checkbox"
                        checked={isHost}
                        onChange={(e) => setIsHost(e.target.checked)}
                    />
                    Register as Host
                </label>
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;