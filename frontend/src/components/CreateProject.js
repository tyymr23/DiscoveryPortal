import React, { useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "./Dialog";
import { Button } from "./Button";
import { Input } from "./Input";
import { Textarea } from "./TextArea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./Select";

const CreateProject = () => {
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("userRole");
  const [client, setClient] = useState("");
  const [clients, setClients] = useState([]);

  const [formData, setFormData] = useState({
    longTitle: "",
    shortTitle: "",
    abstract: "",
    description: "",
    publisher: username,
    deliverables: "",
    impact: "",
    skills: "",
    keywords: "",
    projectType: "",
    semester: "",
  });

  const [semesters, setSemesters] = useState([]);

  useEffect(() => {
    getSemesters();
    getClients();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSemesterChange = (value) => {
    setFormData((prevData) => ({
      ...prevData,
      semester: value,
    }));
  };

  const handleCreateProject = async () => {
    if (
      !formData.longTitle ||
      !formData.shortTitle ||
      !formData.abstract ||
      !formData.description ||
      !formData.deliverables ||
      !formData.impact ||
      !formData.skills ||
      !formData.keywords ||
      !formData.publisher ||
      !formData.projectType ||
      !formData.semester
    ) {
      toast.error("All fields are required");
      return;
    }

    try {
      const keywordsArray = formData.keywords.split(',').map(keyword => keyword.trim());
      const response = await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/project`,
        {
          longTitle: formData.longTitle,
          shortTitle: formData.shortTitle,
          abstract: formData.abstract,
          description: formData.description,
          publisher: role !== "admin" ? username : { client },
          deliverables: formData.deliverables,
          impact: formData.impact,
          skills: formData.skills,
          keywords: keywordsArray,
          projectType: formData.projectType,
          semester: formData.semester,
        }
      );
      toast.success("Project created successfully");
    } catch (error) {
      console.log(error);
      toast.error("Failed to create project");
    }
  };

  const handleReset = () => {
    setFormData({
      longTitle: "",
      shortTitle: "",
      abstract: "",
      description: "",
      publisher: "",
      deliverables: "",
      impact: "",
      skills: "",
      keywords: "",
      projectType: "",
      semester: "",
    });
  };

  const getSemesters = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_BASE_URL}/opensemesters`
      );
      setSemesters(response.data);
    } catch (error) {
      console.error("Error fetching semesters:", error);
    }
  };

  const getClients = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_BASE_URL}/clients`
      );

      setClients(response.data || []);
    } catch (error) {
      console.error("Error fetching clients:", error);
    }
  };

  return (
    <div>
      <ToastContainer position="top-center" />
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Create Project</Button>
        </DialogTrigger>
        <DialogContent className="min-w-[80vw]">
          <DialogHeader>
            <DialogTitle>Create Project</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <div className="flex w-full gap-2">
            <Input
              type="text"
              name="longTitle"
              placeholder="Enter Long Title"
              value={formData.longTitle}
              onChange={handleInputChange}
              className="max-w-full"
            />
            <Input
              type="text"
              name="shortTitle"
              placeholder="Enter Short Title"
              value={formData.shortTitle}
              onChange={handleInputChange}
              className="max-w-full"
            />
          </div>
          <div className="flex w-full gap-2">
            <Textarea
              name="abstract"
              placeholder="Enter Abstract"
              value={formData.abstract}
              onChange={handleInputChange}
              className="max-w-full"
            />
            <Textarea
              name="description"
              placeholder="Enter Description"
              value={formData.description}
              onChange={handleInputChange}
              className="max-w-full"
            />
          </div>
          <div className="flex w-full gap-2">
            <Textarea
              name="deliverables"
              placeholder="Enter Deliverables"
              value={formData.deliverables}
              onChange={handleInputChange}
              className="max-w-full"
            />
            <Textarea
              name="impact"
              placeholder="Enter Impact"
              value={formData.impact}
              onChange={handleInputChange}
              className="max-w-full"
            />
          </div>

          <div className="flex w-full gap-2">
            <Textarea
              name="keywords"
              placeholder="Enter Keywords"
              value={formData.keywords}
              onChange={handleInputChange}
              className="max-w-full"
            />
          </div>

          <div className="flex w-full gap-2">
            <Input
              type="text"
              name="skills"
              placeholder="Enter Skills"
              value={formData.skills}
              onChange={handleInputChange}
              className="max-w-sm"
            />
            <Input
              type="text"
              name="projectType"
              placeholder="Enter Project Type"
              value={formData.projectType}
              onChange={handleInputChange}
              className="max-w-sm"
            />
            <Select
              value={formData.semester}
              onValueChange={handleSemesterChange}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select Semester" />
              </SelectTrigger>
              <SelectContent>
                {semesters.map((semester) => (
                  <SelectItem
                    key={semester.semester_id}
                    value={semester.semester_id.toString()}
                  >
                    {semester.semester} {semester.year}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {role === "admin" && (
              <Select value={client} onValueChange={setClient}>
                <SelectTrigger>
                  <SelectValue placeholder="Select Client" />
                </SelectTrigger>
                <SelectContent>
                  {clients.map((client) => (
                    <SelectItem
                      key={client.username}
                      value={client.username.toString()}
                    >
                      {client.first_name} {client.last_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          </div>
          <div className="flex w-full justify-end gap-2">
            <Button variant="outline" onClick={handleReset}>
              Reset
            </Button>
            <Button onClick={handleCreateProject}>Create Project</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CreateProject;
