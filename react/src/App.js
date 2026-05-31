import { createBrowserRouter, RouterProvider } from 'react-router';
import './App.css';
import GalleryHome from './pages/GalleryHome';
import Picture from './pages/Picture';


function App() {
  const router = createBrowserRouter(
    [
      {path: "/", Component: GalleryHome}, 
      {path: "/picture", Component: Picture}
    ], 
    {basename: "/gallery"}
  );

  return (
    <RouterProvider router={router} />
  );
}

export default App;
