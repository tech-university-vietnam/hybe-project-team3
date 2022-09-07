import { Footer } from "layouts/Footer/Footer";
import { Header } from "layouts/Header/Header";
import { HomePage } from "pages/HomePage/HomePage"
import Register from "pages/Register/Register";
import Login from "pages/Login/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


const App = () => (
  <Router>
    <Routes>
      <Route
        path='/'
        element={<HomePage />}
      />
      <Route
        path='/login'
        element={<Login />}
      />
      <Route
        path='/register'
        element={<Register />}
      />
    </Routes>
  </Router>
)

export default App;
