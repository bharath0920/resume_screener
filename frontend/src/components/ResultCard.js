import React from "react";
import { Card, CardContent, Typography, Alert } from "@mui/material";

export default function ResultCard({ result }) {
  if (result.error) {
    return <Alert severity="error">{result.error}</Alert>;
  }
  return (
    <Card style={{ marginTop: 32 }}>
      <CardContent>
        <Typography variant="h6">Screening Result</Typography>
        <Typography><b>Name:</b> {result.name}</Typography>
        <Typography><b>Email:</b> {result.email}</Typography>
        <Typography><b>Summary:</b> {result.summary}</Typography>
        <Typography><b>Eligible:</b> {result.eligible ? "Yes" : "No"}</Typography>
        <Typography><b>Reason:</b> {result.reason}</Typography>
      </CardContent>
    </Card>
  );
} 