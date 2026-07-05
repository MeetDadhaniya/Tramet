// App.jsx — Root component: defines route structure, applies global layout (Navbar/Footer), and handles top-level error boundaries
import Login from "./pages/auth/Login";

function App() {
  return (
    <main>
      <Login />
    </main>
  );
}

export default App;