import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="bg-slate-900 p-5 flex justify-between">

      <h1 className="text-2xl font-bold text-white">
        Distributed Storage
      </h1>

      <button
        onClick={logout}
        className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded text-white"
      >
        Logout
      </button>

    </div>
  );
}