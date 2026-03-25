import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [qrCode, setQrCode] = useState(null);
  const [error, setError] = useState(null);

  const generateQRCode = async () => {
    setError(null);
    setQrCode(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate_qr_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const errData = await response.json();
        setError(errData.error || "Failed to generate QR code");
        return;
      }

      const data = await response.json();
      setQrCode(data.qr_code);
    } catch (err) {
      setError("Network error: " + err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>QR Code Generator</h1>
      <input
        type="text"
        placeholder="Enter text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ padding: "0.5rem", width: "300px" }}
      />
      <button
        onClick={generateQRCode}
        style={{ marginLeft: "1rem", padding: "0.5rem 1rem" }}
      >
        Generate
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {qrCode && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Your QR Code:</h2>
          <img
            src={`data:image/png;base64,${qrCode}`}
            alt="Generated QR"
            style={{ border: "1px solid #ccc", padding: "10px" }}
          />
        </div>
      )}
    </div>
  );
}

export default App;