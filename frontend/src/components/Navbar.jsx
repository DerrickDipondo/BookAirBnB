import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav>
            <Link to='/'>Home</Link>
            {user ? (
                <>
                <span> | </span>
                <Link to='/bookings'>My Bookings</Link>
                <span> | </span>
                {user.is_host && <Link to="/create-listing">Create Listing</Link>}
                {user.is_host && <span> | </span>}
                {user.is_admin && <Link to="/admin">Admin</Link>}
                {user.is_admin && <span> | </span>}
                <button onClick={logout}>Logout</button>
                </>
            ) : (
                <>
                <span> | </span>
                <Link to='/login'>Login</Link>
                <span> | </span>
                <Link to='/register'>Register</Link>

                </>
            )}
        </nav>
    );
}

export default Navbar;