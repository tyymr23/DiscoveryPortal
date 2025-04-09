import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import axios from "axios";
import { Card, CardHeader, CardTitle, CardContent } from "./Card";
import { Button } from "./Button";
import EditProject from "./EditProject";
import RunButton from "./RunButton";

const CollectionDetails = () => {
  const [formData, setFormData] = useState({
    longTitle: "",
    shortTitle: "",
    abstract: "",
    description: "",
    authors: [],
    date: "",
    publisher: "",
    keywords: [],
    client: "",
    deliverables: "",
    impact: "",
    skills: "",
    projectType: "",
    semester: "",
    year: "",
  });
  const [loading, setLoading] = useState(true);
  const { collectionName } = useParams();
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [userRole, setUserRole] = useState("");
  const firstName = localStorage.getItem("firstName");
  const lastName = localStorage.getItem("lastName");
  const authorName = `${lastName}, ${firstName}`;
  const username = localStorage.getItem("username");
  const [userProject, setUserProject] = useState(
    localStorage.getItem("project") || ""
  );
  const navigate = useNavigate();
  const [runConfig, setRunConfig] = useState({ // required fields for run configuration
    zipFile: null,
    projectName: collectionName || "",
    volumes: "{}",
    frontendPort: "",
    dockerfilePath: "",
  });

  useEffect(() => { // just to make sure the collection name is always the project name for API use
    setRunConfig((prev) => ({ ...prev, projectName: collectionName }));
  }, [collectionName]);

  useEffect(() => {
    const role = localStorage.getItem("userRole");
    setUserRole(role);

    const fetchCollectionDetails = async () => {
      try {
        const response = await fetch(
          `${
            process.env.REACT_APP_API_BASE_URL
          }/collections?project=${encodeURIComponent(collectionName)}`
        );
        const data = await response.json();

        setFormData({
          longTitle: data.project_name || "N/A",
          shortTitle: data.short_title || "N/A",
          abstract: data.abstract || "N/A",
          description: data.description || "N/A",
          authors: JSON.parse(data.authors) || [],
          date: data.date || "N/A",
          publisher: data.publisher || "N/A",
          keywords: JSON.parse(data.keywords) || [],
          client: data.client || "N/A",
          deliverables: data.deliverables || "N/A",
          impact: data.impact || "N/A",
          skills: data.skills || "N/A",
          projectType: data.project_type || "N/A",
          semester: data.semester || "N/A",
          year: data.year || "N/A",
        });
      } catch (error) {
        console.error("Error fetching collection details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCollectionDetails();
  }, [collectionName]);

  useEffect(() => {
    // Fetch files from the server
    axios
      .get(`${process.env.REACT_APP_API_BASE_URL}/projects/${collectionName}`)
      .then((response) => {
        setFiles(response.data);
      })
      .catch((error) => {
        console.error("Error fetching files:", error);
      });
  }, [collectionName]);

  if (loading) {
    return <div>Loading details...</div>;
  }

  const joinProject = async () => {
    if (userProject !== "null") {
      alert("You are already assigned to a project and cannot join another.");
      return;
    }
    if (formData.authors.length >= 5) {
      alert("This project already has 5 authors and cannot accept more.");
      return;
    }
    try {
      await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/users/add-project`,
        {
          username: username,
          project: collectionName,
        }
      );
      await axios.put(
        `${process.env.REACT_APP_API_BASE_URL}/collections/${collectionName}/add-author`,
        { author: authorName }
      );
      setFormData((prevFormData) => ({
        ...prevFormData,
        authors: [...prevFormData.authors, authorName],
      }));
      localStorage.setItem("project", collectionName);
      setUserProject(collectionName);
      alert("You have successfully joined the project!");
    } catch (error) {
      console.error("Error joining project:", error);
      alert("Failed to join the project!");
    }
  };

  const deleteCollection = async (collectionName) => {
    if (
      window.confirm(
        `Are you sure you want to delete the project: ${collectionName}?`
      )
    ) {
      try {
        const response = await axios.delete(
          `${process.env.REACT_APP_API_BASE_URL}/collections/delete/${collectionName}`
        );
        await axios.put(
          `${process.env.REACT_APP_API_BASE_URL}/users/remove-project`,
          {
            username: username,
            projectName: collectionName,
          }
        );
        if (response.status === 200) {
          alert("Project deleted successfully");
          navigate("/home");
        }
      } catch (error) {
        alert(`Error deleting project: ${error.message}`);
      }
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]); // Assuming single file upload
  };

  // Function to handle file upload
  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const fileFormData = new FormData();
    fileFormData.append("files", selectedFile); // 'files' is the key expected by the server

    try {
      setLoading(true); // Optional: Set loading state to show a loading indicator
      const uploadResponse = await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/upload/${collectionName}`,
        fileFormData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // If the upload is successful, re-fetch the files
      if (uploadResponse.status === 201) {
        const filesResponse = await axios.get(
          `${process.env.REACT_APP_API_BASE_URL}/projects/${collectionName}`
        );
        setFiles(filesResponse.data); // Update the files in the state
        alert("File uploaded successfully");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file");
    } finally {
      setLoading(false); // Optional: Clear loading state
      setSelectedFile(null); // Clear the selected file
    }
  };

  // these handle the updates to the run configs
  const handleRunZipChange = (e) => {
    setRunConfig((prev) => ({ ...prev, zipFile: e.target.files[0] }));
  };
  const handleRunInputChange = (e) => {
    const { name, value } = e.target;
    setRunConfig((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="container mx-auto px-4 py-8 flex-grow">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{collectionName}</CardTitle>
              <RunButton runData={runConfig} />
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Metadata Row */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div>
                    <h3 className="font-semibold text-gray-900">Date</h3>
                    <p className="text-gray-700">{formData.date}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Publisher</h3>
                    <p className="text-gray-700">{formData.publisher}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Client</h3>
                    <p className="text-gray-700">{formData.client}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      Project Type
                    </h3>
                    <p className="text-gray-700">{formData.projectType}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Semester</h3>
                    <p className="text-gray-700">{`${formData.semester} ${formData.year}`}</p>
                  </div>
                </div>

                {/* Abstract and Description */}
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-gray-900">Abstract</h3>
                    <p className="text-gray-700">{formData.abstract}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Description</h3>
                    <p className="text-gray-700">{formData.description}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Project Details</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">
                    Deliverables
                  </h3>
                  <p className="text-gray-700">{formData.deliverables}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Impact</h3>
                  <p className="text-gray-700">{formData.impact}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">
                    Skills Required
                  </h3>
                  <p className="text-gray-700">{formData.skills}</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Keywords</h3>
                  <div className="flex flex-wrap gap-2">
                    {formData.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="bg-gray-100 px-2 py-1 rounded-md text-sm"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Team Members</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {formData.authors.map((author, index) => (
                  <div key={index} className="bg-gray-50 p-3 rounded-lg">
                    {author}
                  </div>
                ))}
              </div>
              {userRole === "student" &&
                (userProject === "null" || userProject == []) &&
                formData.authors.length < 5 && (
                  <Button onClick={joinProject} className="mt-4">
                    Join Project
                  </Button>
                )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Project Files</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {files.map((fileUrl, index) => (
                    <a
                      key={index}
                      href={fileUrl}
                      download
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gray-50 p-3 rounded-lg hover:bg-gray-100 transition-colors flex items-center"
                    >
                      <span className="text-blue-600">
                        {decodeURI(fileUrl.split("/").pop())}
                      </span>
                    </a>
                  ))}
                </div>
                <div className="mt-4 space-y-2">
                  <input
                    type="file"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-gray-50 file:text-gray-700
                      hover:file:bg-gray-100"
                  />
                  <Button onClick={handleFileUpload} disabled={!selectedFile}>
                    Upload File
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Run Project Configuration</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label htmlFor="runZipFile" className="block font-semibold">
                    Zip File: (Select a .zip file containing your project)
                  </label>
                  <input
                    type="file"
                    id="runZipFile"
                    accept=".zip"
                    onChange={handleRunZipChange}
                    className="mt-1 block"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="runVolumes" className="block font-semibold">
                    Volumes (JSON format):
                  </label>
                  <textarea
                    id="runVolumes"
                    name="volumes"
                    value={runConfig.volumes}
                    onChange={handleRunInputChange}
                    placeholder='e.g., {"C:/projects/myproject": "/app"}'
                    className="mt-1 block w-full"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="runFrontendPort" className="block font-semibold">
                    Frontend Port (Enter the frontend port your app runs on):
                  </label>
                  <input
                    type="number"
                    id="runFrontendPort"
                    name="frontendPort"
                    value={runConfig.frontendPort}
                    onChange={handleRunInputChange}
                    placeholder="e.g., 3000"
                    className="mt-1 block w-full"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="runDockerfilePath" className="block font-semibold">
                    Dockerfile Path (Relative path inside the unzipped folder):
                  </label>
                  <input
                    type="text"
                    id="runDockerfilePath"
                    name="dockerfilePath"
                    value={runConfig.dockerfilePath}
                    onChange={handleRunInputChange}
                    placeholder="e.g., ./Dockerfile"
                    className="mt-1 block w-full"
                    required
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {(userRole === "admin" || userRole === "client") && (
            <div className="flex justify-end gap-2">
              <EditProject data={formData} />
              <Button
                onClick={() => deleteCollection(collectionName)}
                className="bg-red-700 hover:bg-red-700/90"
              >
                Delete Project
              </Button>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default CollectionDetails;
