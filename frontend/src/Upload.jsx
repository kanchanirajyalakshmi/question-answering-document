import { useState } from "react";
import axios from "axios";

function Upload() {

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {

    if (!file) {
      setMessage("Please select a file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/documents/upload",
        formData
      );

      setMessage(response.data.message);

    } catch (error) {

      setMessage(
        error.response?.data?.detail ||
        "Upload failed"
      );
    }
  };

  return (

    <div>

      <h2>Multi-Format Document Upload</h2>

      <input
        type="file"
        accept=".pdf,.docx,.pptx,.xlsx,.txt,.csv,.html,.json,.md"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        Upload Document
      </button>

      <p>{message}</p>

    </div>

  );
}

export default Upload;
