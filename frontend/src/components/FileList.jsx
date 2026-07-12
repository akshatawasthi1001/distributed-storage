import { useEffect, useState } from "react";
import api from "../api/axios";

export default function FileList() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await api.get("/files?page=1&limit=20", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setFiles(res.data);

    } catch (err) {
      console.log(err);
      alert("Failed to load files");
    }
  };

  const deleteFile = async (id) => {
    try {
      const token = localStorage.getItem("token");

      await api.delete(`/files/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert("File deleted successfully");

      fetchFiles();

    } catch (err) {
      console.log(err);
      alert("Delete failed");
    }
  };

  return (
    <div className="bg-slate-800 p-6 rounded-xl mt-6">

      <h2 className="text-xl font-bold text-white mb-4">
        My Files
      </h2>

      {files.length === 0 ? (
        <p className="text-gray-400">
          No files uploaded.
        </p>
      ) : (
        files.map((file) => (
          <div
            key={file.id}
            className="bg-slate-700 p-4 rounded-lg mb-3 flex justify-between items-center"
          >
            <div className="text-white">
              <h3 className="font-semibold">
                {file.filename}
              </h3>

              <p className="text-sm text-gray-300">
                {file.size} bytes
              </p>
            </div>

            <button
              onClick={() => deleteFile(file.id)}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white"
            >
              Delete
            </button>

          </div>
        ))
      )}

    </div>
  );
}