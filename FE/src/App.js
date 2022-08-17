import { useEffect, useState } from "react";
import "./App.css";
const axios = require("axios");

function App() {
  const [data, setData] = useState("");
  const url = "http://localhost:8088/api/day";

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get(url);
      console.log("response is", response);
      setData(response.data.day);
    };
    fetchData();
  }, [data]);

  return (
    <div className="App">
      <p>HYBE app page</p>
      <p>{data}</p>
    </div>
  );
}

export default App;
