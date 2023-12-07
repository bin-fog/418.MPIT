import { PrimeReactProvider } from 'primereact/api';
import MPITMenubar from './Components/MPITMenubar';
import MPITDefault from './Components/MPITDefault';
import MPITCard from './Components/MPITCardView';

import { RouterProvider } from 'react-router-dom';
import { createBrowserRouter } from 'react-router-dom';

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: (
        <PrimeReactProvider >
          <MPITMenubar />
          <MPITDefault title="Добро пожаловать" description="Вот чем можно заняться сегодня:"  />
          <MPITCard type="tasks" />
        </PrimeReactProvider>
      ),
    },
    {
      path: "shop",
      element: (
        <PrimeReactProvider >
          <MPITMenubar />
          <MPITDefault title="Магазин" description="За акселькоины можно покупать различные призы:"  />
          <MPITCard type="shop" company="МПИТ"/>
          <MPITCard type="shop" company="Вега"/>
        </PrimeReactProvider>
      ),
    },
  ]);
  return (
    <RouterProvider router={router} />
  );
}

export default App;
