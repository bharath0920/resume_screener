import React, { useState } from "react";
import { TextField, Button, Paper, Typography, CircularProgress } from "@mui/material";
import axios from "axios";
import ResultCard from "./ResultCard";

const API_URL = "http://127.0.0.1:8000/screen_resumes/";

export default function ResumeScreeningForm() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jobDescription || !resumeFile) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("files", resumeFile);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "job-code": "DEMO", // You can make this dynamic if needed
          "position-name": "Demo Position", // You can make this dynamic if needed
        },
      });
      setResult(response.data.results[0]);
    } catch (err) {
      setResult({ error: "Screening failed. Please try again." });
    }
    setLoading(false);
  };

  return (
    <Paper elevation={3} style={{ padding: 32, maxWidth: 600, width: "100%" }}>
      <Typography variant="h5" gutterBottom>
        Resume Screening
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Job Description"
          placeholder="Paste the job description here..."
          multiline
          minRows={6}
          fullWidth
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          margin="normal"
          required
        />
        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={handleFileChange}
          style={{ margin: "16px 0" }}
          required
        />
        <div style={{ marginTop: 16 }}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            fullWidth
            size="large"
          >
            {loading ? <CircularProgress size={24} /> : "Screen Resume"}
          </Button>
        </div>
      </form>
      {result && <ResultCard result={result} />}
    </Paper>
  );
} 