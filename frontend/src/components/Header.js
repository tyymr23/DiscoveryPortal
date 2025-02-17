import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./Button";
const Header = () => {
  const navigate = useNavigate();
  const userRole = localStorage.getItem("userRole");

  const navigateHome = () => {
    if (userRole === "admin") {
      navigate("/home");
    } else if (userRole === "client") {
      navigate("/home");
    } else {
      navigate("/home");
    }
  };

  const handleSignOut = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <header className="bg-maroon shadow-md text-white">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <h1 className="text-xl font-semibold">CS 4624 Discovery Portal</h1>
        <div className="flex space-x-2">
          <Button
            onClick={navigateHome}
            variant="outline"
            className="bg-maroon text-white"
          >
            Home
          </Button>
          <Button
            onClick={handleSignOut}
            variant="outline"
            className="bg-maroon text-white"
          >
            Sign Out
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
