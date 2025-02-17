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

const CurrentProjects = ({ collections, title = "Current Projects" }) => {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between">
          <CardTitle>{title}</CardTitle>
          <div className="text-sm text-gray-500">
            Total Projects: {collections.length}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {collections.length === 0 || !collections ? (
          <div className="text-center w-full">No projects found</div>
        ) : (
          <div className="overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[212px]">Project</TableHead>
                  <TableHead className="w-[700px]">Description</TableHead>
                  <TableHead className="w-[100px] pl-0">Semester</TableHead>
                  <TableHead
                    className={`w-[100px] ${
                      collections.some((collection) => collection.client_name)
                        ? "text-left"
                        : "text-center"
                    }`}
                  >
                    Client
                  </TableHead>
                  <TableHead className="text-center w-[100px]">
                    Team Size
                  </TableHead>
                  <TableHead className="w-[100px]"></TableHead>
                </TableRow>
              </TableHeader>
            </Table>
            <div className="max-h-[55vh] overflow-y-auto">
              <Table>
                <TableBody>
                  {collections.map((collection, index) => (
                    <TableRow key={index} className="group">
                      <TableCell className="w-[212px]">
                        {collection.project_name.length > 20
                          ? collection?.project_name?.substring(0, 20) + "..."
                          : collection?.project_name}
                      </TableCell>
                      <TableCell className="w-[700px]">
                        {collection?.description?.length > 90
                          ? collection?.description?.substring(0, 90) + "..."
                          : collection?.description}
                      </TableCell>
                      <TableCell className="w-[100px] p-0">
                        {collection.semester}
                      </TableCell>
                      <TableCell
                        className={`w-[100px] ${
                          collection.client_name ? "text-left" : "text-center"
                        }`}
                      >
                        {collection.client_name || "N/A"}
                      </TableCell>
                      <TableCell className="text-center w-[100px]">
                        {collection.author_count}
                      </TableCell>
                      <TableCell className="text-center w-[100px]">
                        <Link
                          to={`/collections/${encodeURIComponent(
                            collection.project_name
                          )}`}
                          className="text-blue-600 hover:underline group-hover:bg-gray-50"
                        >
                          <Button>View</Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default CurrentProjects;
