import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isHost, setIsHost] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/register', { email, password, is_host: isHost });
            navigate('/login');
        } catch (err) {
            setError(err.resposnse?.data?.message || 'Registration failed');
            console.log('Registration error:', err.response?.data, err.message); // Debug log
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input 
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
              />
                <input 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
              />
              <label>
                <input 
                    type="checkbox"
                    checked={isHost}
                    onChange={(e) => setIsHost(e.target.checked)}
               />
               Register as Host
              </label>
              <label>
                <button type="submit">Register</button>
              </label>
            </form>
        </div>
    );
}

export default Register;