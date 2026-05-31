import { Link } from "react-router";

export default function GalleryHome() {
    return (
        <>
            <p>Gallery Home Page.</p>
            <Link to="/picture">Go to Pictures</Link>
        </>
    );
};