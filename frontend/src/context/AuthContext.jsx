import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initializeAuth = async () => {
            try {
                const token = localStorage.getItem('token');
                const storedUser = localStorage.getItem('user');
                if (token && storedUser) {
                    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                    try {
                        const response = await axios.get('/api/me');
                        setUser(response.data);
                    } catch (err) {
                        console.warn('Failed to verify token, using stored user:', err.message);
                        try {
                            setUser(JSON.parse(storedUser));
                        } catch (parseErr) {
                            console.error('Invalid stored user data:', parseErr);
                            localStorage.removeItem('user');
                        }
                    }
                }
            } catch (err) {
                console.error('Auth initialization error:', err);
            } finally {
                setLoading(false);
            }
        };
        initializeAuth();
    }, []);

    const login = async (email, password) => {
        try {
            const response = await axios.post('/api/login', { email, password });
            const { access_token, id, is_host, is_admin } = response.data;
            localStorage.setItem('token', access_token);
            localStorage.setItem('user', JSON.stringify({ id, is_host, is_admin }));
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
            setUser({ id, is_host, is_admin });
            return response.data;
        } catch (err) {
            throw new Error(err.response?.data?.message || 'Login failed');
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        delete axios.defaults.headers.common['Authorization'];
        setUser(null);
    };

    const value = { user, login, logout, loading };
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};