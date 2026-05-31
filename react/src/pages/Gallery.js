import { Link } from "react-router";

export default function Gallery() {
    return (
        <>
            <p>Gallery Page.</p>
            <Link to="/picture">Go to Picture</Link>
            <br></br>
            <br></br>
            <a href="/account">Go to account</a>
        </>
    );
};