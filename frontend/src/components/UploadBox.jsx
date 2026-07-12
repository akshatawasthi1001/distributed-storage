import { useState } from "react";
import api from "../api/axios";

export default function UploadBox() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem("token");

      await api.post("/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      alert("File uploaded successfully!");

      setFile(null);

    } catch (err) {
      console.log(err);
      console.log(err.response);

      alert(JSON.stringify(err.response?.data || err.message));
    }
  };

  return (
    <div className="bg-slate-800 p-6 rounded-xl mt-8 text-white">

      <h2 className="text-xl font-bold mb-4">
        Upload File
      </h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 block"
      />

      <button
        onClick={uploadFile}
        className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded"
      >
        Upload
      </button>

    </div>
  );
}