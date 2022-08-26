import { Footer } from "layouts/Footer/Footer";
import { Header } from "layouts/Header/Header";
import { HomePage } from "pages/HomePage/HomePage"
import Register from "pages/Register/Register";
import Login from "pages/Login/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


const App = () => (
  <Router>
    <Header />
    <Routes>
      <Route index element={<Login/>} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
    <Footer />
  </Router>
)

export default App;
