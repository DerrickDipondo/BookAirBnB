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