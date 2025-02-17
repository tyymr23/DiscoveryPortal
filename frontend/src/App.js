import { Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/SignUp";
import Home from "./Home";
import CollectionDetails from "./components/CollectionDetails";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home/*" element={<Home />} />
        <Route
          path="/collections/:collectionName"
          element={<CollectionDetails />}
        />
      </Routes>
    </div>
  );
}

export default App;
