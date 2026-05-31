import { createBrowserRouter, RouterProvider } from 'react-router';
import './App.css';
import Gallery from './pages/Gallery';
import Picture from './pages/Picture';


function App() {
  const router = createBrowserRouter(
    [
      {path: "/gallery", Component: Gallery}, 
      {path: "/picture", Component: Picture}
    ], 
    {basename: "/app"}
  );

  return (
    <RouterProvider router={router} />
  );
}

export default App;
