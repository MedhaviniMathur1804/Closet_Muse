import React, { useState } from 'react';
import axios from 'axios';
import "./App.css";

interface Recommendation {
  name: string;
  category: string;
  image_url: string;
  description: string;
}

interface ApiResponse {
  recommendations: Recommendation[];
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setPreviewUrl(URL.createObjectURL(event.target.files[0]));
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post<ApiResponse>("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      alert("Error uploading image or fetching recommendations.");
    }
  };

  return (
    <div className="container">
      {/* Left: Upload */}
      <div className="left-panel">
        <h2>Upload Image</h2>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        {previewUrl && (
          <div className="image-preview">
            <img src={previewUrl} alt="Preview" />
          </div>
        )}
        <button onClick={handleUpload} disabled={!selectedFile}>
          Get Recommendations
        </button>
      </div>

      {/* Divider */}
      <div className="divider" />

      {/* Right: Output */}
      <div className="right-panel">
        <h2>Recommendations</h2>
        {Object.keys(recommendations).length === 0 ? (
          <p>No recommendations yet.</p>
        ) : (
          Object.entries(recommendations).map(([category, recs]) => (
            <div key={category}>
              <h3>{category.charAt(0).toUpperCase() + category.slice(1)}</h3>
              <ul>
                {recs.map((rec, idx) => (
                  <li key={idx}>
                    <strong>{rec.name}</strong> <br />
                    <img src={rec.image_url} alt={rec.name} style={{ maxWidth: "100px" }} />
                    <br />
                    <span>{rec.description}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App; 