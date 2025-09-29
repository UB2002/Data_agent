import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:3000", // backend URL
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const askQuestion = async (sessionId, question) => {
  const res = await API.post("/ask", { session_id: sessionId, question });
  return res.data;
};
