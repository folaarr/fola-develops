import { Link } from "react-router";

export default function GalleryHome() {
    return (
        <>
            <p>Gallery Page.</p>
            <Link to="/picture">Go to Picture</Link>
            <br></br>
            <br></br>
            <Link to="http://127.0.0.1:5000/account">Go to account</Link>
        </>
    );
};