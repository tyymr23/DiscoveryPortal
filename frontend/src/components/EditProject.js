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

const EditProject = ({ data }) => {
  const username = localStorage.getItem("username");
  const [formData, setFormData] = useState({
    longTitle: data?.longTitle,
    // shortTitle: data?.shortTitle,
    abstract: data?.abstract,
    description: data?.description,
    publisher: username,
    deliverables: data?.deliverables,
    impact: data?.impact,
    skills: data?.skills,
    keywords: data?.keywords,
    projectType: data?.projectType,
    semester: data?.semester + ` ${data?.year}`,
  });

  const [semesters, setSemesters] = useState([]);

  useEffect(() => {
    getSemesters();
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

  const handleUpdateProject = async () => {
    if (
      !formData.longTitle ||
      // !formData.shortTitle ||
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

    // from logan: use the old project name, works simarly to create project route
    try {
      console.log(formData)
      let keywordsArray;
      if (Array.isArray(formData.keywords)) {
        keywordsArray = formData.keywords;
      } else {
        keywordsArray = formData.keywords.split(',').map(keyword => keyword.trim());
      }
      const response = await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/collection/edit?project_name=${encodeURIComponent(data.longTitle)}`,
        {
          longTitle: formData.longTitle,
          // shortTitle: formData.shortTitle,
          abstract: formData.abstract,
          description: formData.description,
          publisher: username,
          deliverables: formData.deliverables,
          impact: formData.impact,
          skills: formData.skills,
          keywords: keywordsArray, // "lists" are stored as strings in sql
          projectType: formData.projectType,
          semester: formData.semester,
        }
      );
      toast.success("Project updated successfully");
    } catch (error) {
      console.log(error);
      toast.error("Failed to update project");
    }
  };

  // same
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

  return (
    <div>
      <ToastContainer position="top-center" />
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Edit Project</Button>
        </DialogTrigger>
        <DialogContent className="min-w-[80vw]">
          <DialogHeader>
            <DialogTitle>Edit Project</DialogTitle>
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
                    value={semester.semester + ` ${semester.year}`}
                  >
                    {semester.semester} {semester.year}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex w-full justify-end gap-2">
            <Button onClick={handleUpdateProject}>Update Project</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EditProject;
