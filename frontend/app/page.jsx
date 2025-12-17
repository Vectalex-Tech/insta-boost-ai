"use client";

import { useMemo, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Page() {
  const [project, setProject] = useState(null);
  const [prompt, setPrompt] = useState("Cria um Reel curto com 3 dicas práticas para melhorar retenção no Instagram.");
  const [niche, setNiche] = useState("marketing digital");
  const [file, setFile] = useState(null);
  const [packaging, setPackaging] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState("");

  async function createProject() {
    setStatus("A criar projeto...");
    const r = await fetch(`${API}/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "New project", prompt, niche, goal: "reach" }),
    });
    const data = await r.json();
    setProject(data);
    setStatus("Projeto criado.");
  }

  async function uploadVideo() {
    if (!project || !file) return;
    setStatus("A fazer upload...");
    const fd = new FormData();
    fd.append("project_id", project.id);
    fd.append("kind", "video");
    fd.append("file", file);
    const r = await fetch(`${API}/assets`, { method: "POST", body: fd });
    await r.json();
    setStatus("Upload feito.");
  }

  async function generate() {
    if (!project) return;
    setStatus("A gerar packaging com IA...");
    const r = await fetch(`${API}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: project.id, language: "pt", tone: "direto", max_duration_sec: 18 }),
    });
    const data = await r.json();
    setPackaging(data.packaging);
    setStatus("Packaging gerado.");
  }

  async function render() {
    if (!project) return;
    setStatus("A renderizar (job async)...");
    const r = await fetch(`${API}/render`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: project.id, variant: "A", burn_captions: false }),
    });
    const data = await r.json();
    setTaskId(data.task_id);
    setStatus(`Job criado: ${data.task_id}. (ver logs do worker)`);
  }

  async function refreshProject() {
    if (!project) return;
    const r = await fetch(`${API}/projects/${project.id}`);
    const data = await r.json();
    setProject(data);
    setStatus(`Status: ${data.status}`);
  }

  async function publish() {
    if (!project) return;
    setStatus("A publicar via Graph API...");
    const r = await fetch(`${API}/instagram/publish`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ project_id: project.id, media_type: "REELS" }),
    });
    const data = await r.json();
    setStatus(JSON.stringify(data, null, 2));
  }

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <div style={{ display: "grid", gap: 8, padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
        <label>Prompt</label>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={4} style={{ width: "100%" }} />
        <label>Nicho</label>
        <input value={niche} onChange={(e) => setNiche(e.target.value)} />
        <button onClick={createProject}>1) Criar projeto</button>
      </div>

      <div style={{ display: "grid", gap: 8, padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
        <label>Upload de vídeo (para o MVP o render espera um vídeo)</label>
        <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={uploadVideo} disabled={!project || !file}>2) Upload vídeo</button>
      </div>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <button onClick={generate} disabled={!project}>3) Gerar packaging</button>
        <button onClick={render} disabled={!project}>4) Render (Celery)</button>
        <button onClick={refreshProject} disabled={!project}>Atualizar status</button>
        <button onClick={publish} disabled={!project}>5) Publicar</button>
      </div>

      <pre style={{ whiteSpace: "pre-wrap", background: "#fafafa", padding: 12, borderRadius: 12, border: "1px solid #eee" }}>
        {status}
      </pre>

      {packaging && (
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
          <h2>Packaging</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(packaging, null, 2)}</pre>
        </div>
      )}

      {project?.render_json?.render?.output_path && (
        <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 12 }}>
          <h2>Output render (dev)</h2>
          <video controls style={{ width: "100%" }} src={`${API}/static/renders/${project.render_json.render.output_path.split("/").pop()}`} />
        </div>
      )}
    </div>
  );
}
