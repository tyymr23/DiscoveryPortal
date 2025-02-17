import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "./Dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./Select";
import { Button } from "./Button";
import axios from "axios";
import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import { formatSemesterStatus } from "../lib/utils";

const EditSemester = ({ flag }) => {
  const [semester, setSemester] = useState("");
  const [semesters, setSemesters] = useState([]);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    getSemesters();
  }, [flag, refresh]);

  const getSemesters = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_BASE_URL}/semesters`
      );
      setSemesters(response.data);
    } catch (error) {
      console.error("Error fetching semesters:", error);
    }
  };

  const handleCloseSemester = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_BASE_URL}/semester/close`, {
        year: semester.year,
        semester: semester.semester,
      });
      toast.success("Semester closed successfully");
    } catch (error) {
      toast.error("Failed to close semester");
    } finally {
      setRefresh(!refresh);
    }
  };

  const handleOpenSemester = async () => {
    try {
      await axios.post(`${process.env.REACT_APP_API_BASE_URL}/semester/open`, {
        year: semester.year,
        semester: semester.semester,
      });
      toast.success("Semester opened successfully");
    } catch (error) {
      toast.error("Failed to open semester");
    } finally {
      setRefresh(!refresh);
    }
  };

  return (
    <div>
      <ToastContainer position="top-center" />
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Open/Close Semester</Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Open/Close Semester</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <div className="flex gap-2">
            <Select value={semester} onValueChange={setSemester}>
              <SelectTrigger>
                <SelectValue placeholder="Select Semester" />
              </SelectTrigger>
              <SelectContent>
                {semesters.map((semester) => (
                  <SelectItem key={semester.semester_id} value={semester}>
                    {semester.semester} {semester.year} (
                    {formatSemesterStatus(semester.status)})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {semester && semester.status === "open" && (
              <Button onClick={handleCloseSemester}>Close</Button>
            )}
            {semester && semester.status === "close" && (
              <Button onClick={handleOpenSemester}>Open</Button>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EditSemester;
