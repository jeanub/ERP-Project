import React, { useState } from "react";
import { useAuth } from "../auth/AuthProvider";
import api from "../lib/api"; 

export default function Login() {
  const { login } = useAuth();
  const [u, setU] = useState("jean");
  const [p, setP] = useState("jean123k");
  const [err, setErr] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr("");
    const ok = await login(u, p);
    if (!ok) setErr("Credenciales inválidas");
    else window.location.href = "/"; // a productos
  };

  return (
    <div className="min-h-screen grid place-items-center p-6">
      <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 p-6 rounded-2xl shadow">
        <h1 className="text-xl font-semibold">Iniciar sesión</h1>
        <input className="w-full border rounded px-3 py-2" value={u} onChange={e=>setU(e.target.value)} placeholder="Usuario" />
        <input className="w-full border rounded px-3 py-2" type="password" value={p} onChange={e=>setP(e.target.value)} placeholder="Contraseña" />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="w-full bg-black text-white rounded py-2">Entrar</button>
      </form>
    </div>
  );
}
