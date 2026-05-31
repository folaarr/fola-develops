import { createBrowserRouter, RouterProvider } from 'react-router';
import './App.css';
import GalleryHome from './pages/GalleryHome';
import Picture from './pages/Picture';


function App() {
  const router = createBrowserRouter([
    {path: "/gallery", Component: GalleryHome}, 
    {path: "/picture", Component: Picture}
  ]);

  return (
    <RouterProvider router={router} />
  );
}

export default App;
