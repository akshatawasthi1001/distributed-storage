import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import SearchBar from "../components/SearchBar";
import FileList from "../components/FileList";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-950">

      <Navbar />

      <div className="max-w-6xl mx-auto p-8">

        <UploadBox />

        <SearchBar />

        <FileList />

      </div>

    </div>
  );
}