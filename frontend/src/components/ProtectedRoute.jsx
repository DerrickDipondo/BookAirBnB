import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function ProtectedRoute({ children, requireHost = false, requireAdmin = false }) {
    const { user, loading } = useAuth();

    if (loading) {
        return <p>Loading...</p>;
    }

    if (!user) {
        return <Navigate to="/login" />;
    }
    if (requireHost && !user.is_host) {
        return <Navigate to="/" />;
    }
    if (requireAdmin && !user.is_admin) {
        return <Navigate to="/" />;
    }
    return children;
}

export default ProtectedRoute;