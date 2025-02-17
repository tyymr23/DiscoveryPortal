import { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { Button } from "./components/Button";
import axios from "axios";
import Header from "./components/Header";
import Footer from "./components/Footer";
import CurrentProjects from "./components/CurrentProjects";
import YourProjects from "./components/YourProjects";
import AdminControls from "./components/AdminControls";
import { Input } from "./components/Input";
import CreateProject from "./components/CreateProject";

function Home() {
  const navigate = useNavigate();
  const [collections, setCollections] = useState([]);
  const [filteredCollections, setFilteredCollections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userProjects, setUserProjects] = useState([]);
  const [username, setUsername] = useState(
    localStorage.getItem("username") || ""
  );
  const [searchTerm, setSearchTerm] = useState("");
  const [semester, setSemester] = useState("");
  const firstName = localStorage.getItem("firstName");
  const lastName = localStorage.getItem("lastName");
  const authorName = `${lastName}, ${firstName}`;
  const userRole = localStorage.getItem("userRole");

  useEffect(() => {
    if (!userRole) {
      navigate("/");
    }
    const fetchCollections = async () => {
      setLoading(true);
      try {
        if (userRole === "admin") {
          if (username) {
            try {
              const response = await fetch(
                `${
                  process.env.REACT_APP_API_BASE_URL
                }/collections?username=${encodeURIComponent(username)}`
              );
              const data = await response.json();

              setCollections(data.projects);
              setFilteredCollections(data.projects);
            } catch (error) {
              console.error("Error fetching user data:", error);
            }
          }
        } else {
          const response = await fetch(
            `${process.env.REACT_APP_API_BASE_URL}/collections`
          );
          const data = await response.json();
          setCollections(data);
          setFilteredCollections(data);
        }
      } catch (error) {
        console.error("Error fetching collections:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCollections();
  }, []);

  useEffect(() => {
    const results = collections.filter(
      (collection) =>
        collection.project_name
          ?.toLowerCase()
          .includes(searchTerm.toLowerCase()) ||
        collection.description
          ?.toLowerCase()
          .includes(searchTerm.toLowerCase()) ||
        collection.client_name
          ?.toLowerCase()
          .includes(searchTerm.toLowerCase()) ||
        collection.semester?.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredCollections(results);
  }, [searchTerm, collections]);

  useEffect(() => {
    const fetchUserData = async () => {
      if (username) {
        try {
          const response = await fetch(
            `${
              process.env.REACT_APP_API_BASE_URL
            }/collections?username=${encodeURIComponent(username)}`
          );
          const data = await response.json();

          let projects = [];
          if (data.user && data.user.projects) {
            if (typeof data.user.projects === "string") {
              try {
                // Try to parse the string as JSON
                projects = JSON.parse(data.user.projects);
              } catch (parseError) {
                console.error("Error parsing projects string:", parseError);
                projects = [data.user.projects];
              }
            } else if (Array.isArray(data.user.projects)) {
              projects = data.user.projects;
            } else if (typeof data.user.projects === "object") {
              projects = [data.user.projects];
            }
          }

          // Ensure projects is always an array of objects
          projects = projects.map((project) => {
            if (typeof project === "string") {
              try {
                return JSON.parse(project);
              } catch (parseError) {
                console.error("Error parsing individual project:", parseError);
                return { project_name: project };
              }
            }
            return project;
          });

          setUserProjects(projects);
        } catch (error) {
          console.error("Error fetching user data:", error);
        }
      }
    };

    fetchUserData();
  }, [username]);

  if (loading) return <div>Loading projects...</div>;

  const leaveProject = async (projectName) => {
    if (!projectName) {
      alert("Invalid project name.");
      return;
    }

    if (!window.confirm("Are you sure you want to leave this project?")) {
      return;
    }

    try {
      const removeProjectResponse = await axios.put(
        `${process.env.REACT_APP_API_BASE_URL}/users/remove-project`,
        {
          username: username,
          projectName: projectName,
        }
      );

      if (removeProjectResponse.data.success) {
        const removeAuthorResponse = await axios.delete(
          `${process.env.REACT_APP_API_BASE_URL}/collections/${projectName}/remove-author`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            data: {
              author: authorName,
            },
          }
        );

        if (
          removeAuthorResponse.data.message === "Author removed successfully"
        ) {
          // Update local UI state
          setUserProjects(
            userProjects.filter((project) => project !== projectName)
          ); // Remove project from array
          localStorage.setItem("project", "null");
          alert("You have successfully left the project.");
        } else {
          throw new Error("Failed to remove author from project.");
        }
      } else {
        throw new Error("Failed to remove project from user.");
      }
    } catch (error) {
      console.error("Error leaving project:", error);
      alert(
        error.response?.data?.error ||
          error.message ||
          "Failed to leave the project."
      );
    }
  };

  return (
    <>
      <Header />
      <div className="flex flex-col min-h-screen">
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route
              path="/"
              element={
                <div className="space-y-8">
                  {userRole === "client" && (
                    <div className="flex justify-between">
                      <CreateProject />
                    </div>
                  )}
                  {userRole === "admin" && (
                    <AdminControls
                      searchTerm={searchTerm}
                      setSearchTerm={setSearchTerm}
                    />
                  )}
                  {userRole === "student" && (
                    <div className="flex justify-start items-center">
                      <Input
                        type="text"
                        placeholder="Search projects..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="max-w-sm"
                      />
                    </div>
                  )}
                  {userRole !== "client" && (
                    <CurrentProjects
                      collections={filteredCollections}
                      title={
                        userRole === "admin"
                          ? "All Projects"
                          : "Current Projects"
                      }
                    />
                  )}
                  {(userRole === "student" || userRole === "client") && (
                    <YourProjects
                      userProjects={userProjects}
                      leaveProject={leaveProject}
                    />
                  )}
                </div>
              }
            />
          </Routes>
        </main>
        <Footer />
      </div>
    </>
  );
}

export default Home;
