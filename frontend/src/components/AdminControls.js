import { Input } from "./Input";
import CreateProject from "./CreateProject";
import CreateSemester from "./CreateSemester";
import CreateUser from "./CreateUser";
import EditSemester from "./EditSemester";
import { useState } from "react";

const AdminControls = ({ searchTerm, setSearchTerm }) => {
  const [flag, setFlag] = useState(false);
  return (
    <div className="flex justify-between items-center">
      <div className="flex justify-start gap-2">
        <CreateUser />
        <CreateProject />
        <CreateSemester flag={flag} setFlag={setFlag} />
        <EditSemester flag={flag} />
      </div>
      <Input
        type="text"
        placeholder="Search projects..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="max-w-sm"
      />
    </div>
  );
};

export default AdminControls;
