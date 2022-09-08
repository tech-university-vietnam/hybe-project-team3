import { Footer } from "layouts/Footer/Footer";
import { Header } from "layouts/Header/Header";
import { HomePage } from "pages/HomePage/HomePage"
import Register from "pages/Register/Register";
import Login from "pages/Login/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "Utils/hooks/auth";
import RequireAuth from "Utils/routes/RequireAuth";
import UnauthedOnly from "Utils/routes/UnauthedOnly";


const App = () => (
  <AuthProvider>
    <Router>
      <Routes>
        <Route
          path='/'
          element={
            <RequireAuth>
              <HomePage />
            </RequireAuth>
          }
        />
        <Route
          path='/login'
          element={
            <UnauthedOnly>
              <Login />
            </UnauthedOnly>
          }
        />
        <Route
          path='/register'
          element={
            <UnauthedOnly>
              <Register/>
            </UnauthedOnly>
          }
        />
      </Routes>
    </Router>
  </AuthProvider>
)

export default App;
