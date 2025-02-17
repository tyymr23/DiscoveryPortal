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
import { Input } from "./Input";
import axios from "axios";
import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";

const CreateSemester = ({ flag, setFlag }) => {
  const [year, setYear] = useState("");
  const [season, setSeason] = useState("");

  const handleCreateSemester = async () => {
    if (!year || !season) {
      toast.error("All fields are required");
      return;
    }
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_BASE_URL}/semester/create`,
        {
          year: year,
          semester: season,
          status: "open",
        }
      );
      toast.success("Semester created successfully");
      setFlag(!flag);
    } catch (error) {
      toast.error("Failed to create semester");
    }
  };

  return (
    <div>
      <ToastContainer position="top-center" />
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Create Semester</Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create Semester</DialogTitle>
            <DialogDescription></DialogDescription>
          </DialogHeader>
          <div className="flex gap-2">
            <Select value={season} onValueChange={setSeason}>
              <SelectTrigger>
                <SelectValue placeholder="Select Season" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Fall">Fall</SelectItem>
                <SelectItem value="Spring">Spring</SelectItem>
              </SelectContent>
            </Select>
            <Input
              type="text"
              placeholder="Enter Year"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              className="max-w-sm"
            />
            <Button onClick={handleCreateSemester}>Create</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default CreateSemester;
