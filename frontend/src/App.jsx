import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Listings from './components/Listings';
import CreateListing from './components/CreateListing';
import Bookings from './components/Bookings';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
    return (
        <AuthProvider>
            <div className="App">
                <Navbar />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/" element={<Listings />} />
                    <Route
                        path="/create-listing"
                        element={
                            <ProtectedRoute requireHost>
                                <CreateListing />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/bookings"
                        element={
                          <ProtectedRoute>
                            <Bookings />
                          </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/admin"
                        element={
                            <ProtectedRoute requireAdmin>
                                <h2>Admin Dashboard</h2>
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </div>
        </AuthProvider>
    );
}

export default App;