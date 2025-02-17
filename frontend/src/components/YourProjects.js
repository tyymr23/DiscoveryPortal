import { Card, CardHeader, CardTitle, CardContent } from "./Card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./Table";
import { Button } from "./Button";
import { Link } from "react-router-dom";

const YourProjects = ({ userProjects, leaveProject }) => {
  const userRole = localStorage.getItem("userRole");

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Projects</CardTitle>
      </CardHeader>
      <CardContent>
        {userProjects &&
        userProjects.some((project) => project?.project_name) ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Project</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Semester</TableHead>
                <TableHead
                  className={
                    userProjects.some((project) => project?.client_name)
                      ? ""
                      : "text-center"
                  }
                >
                  Client
                </TableHead>
                <TableHead className="text-center">Team Size</TableHead>
                <TableHead></TableHead>
                {userRole === "student" && <TableHead></TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {userProjects.map((project, index) => (
                <TableRow className="group" key={index}>
                  <TableCell>{project?.project_name}</TableCell>
                  <TableCell>
                    {project?.description?.length > 50
                      ? project?.description?.substring(0, 50) + "..."
                      : project?.description}
                  </TableCell>
                  <TableCell>
                    {project?.semester} {project?.year}
                  </TableCell>
                  <TableCell
                    className={project.client_name ? "" : "text-center"}
                  >
                    {project?.publisher || "N/A"}
                  </TableCell>
                  <TableCell className="text-center">
                    {project?.author_count}
                  </TableCell>
                  <TableCell className="text-center">
                    <Link
                      to={`/collections/${encodeURIComponent(
                        project?.project_name
                      )}`}
                      className="text-blue-600 hover:underline group-hover:bg-gray-50"
                    >
                      <Button>View</Button>
                    </Link>
                  </TableCell>
                  {userRole === "student" && (
                    <TableCell className="text-center px-0">
                      <Button
                        onClick={() => leaveProject(project?.project_name)}
                        variant="outline"
                        className="text-red-800"
                      >
                        Leave Project
                      </Button>
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <div className="text-center w-full">You don't have any projects</div>
        )}
      </CardContent>
    </Card>
  );
};

export default YourProjects;
