import { useEffect, useState } from "react";
import api from "../lib/api";
import { useAuth } from "../auth/AuthProvider";
import { useNavigate } from "react-router-dom";

type Product = { id:number; sku:string; name:string; price:string; stock:number };

export default function Products() {
  const [items, setItems] = useState<Product[]>([]);
  const [form, setForm] = useState({ sku: "", name: "", price: "0.00", stock: 0 });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const { logout } = useAuth();
  const nav = useNavigate();

  async function load() {
    setLoading(true);
    const { data } = await api.get("/products/");
    setItems(data.results ?? data);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  async function create(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post("/products/", form);           
      setForm({ sku: "", name: "", price: "0.00", stock: 0 });
      await load();
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Error creando producto");
    } finally { setSubmitting(false); }
  }

  function doLogout() {
    logout();                                        // borra tokens
    nav("/login", { replace: true });               // vuelve a /login
  }

  if (loading) return <p>Cargando...</p>;

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Productos</h1>
        <button className="text-sm underline" onClick={doLogout}>Salir</button>
      </header>

      <form onSubmit={create} className="grid grid-cols-5 gap-2 items-end">
        <input className="border rounded px-2 py-1" placeholder="SKU"
          value={form.sku} onChange={e => setForm({ ...form, sku: e.target.value })} />
        <input className="border rounded px-2 py-1 col-span-2" placeholder="Nombre"
          value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <input className="border rounded px-2 py-1" placeholder="Precio"
          value={form.price} onChange={e => setForm({ ...form, price: e.target.value })} />
        <input className="border rounded px-2 py-1" placeholder="Stock" type="number"
          value={form.stock} onChange={e => setForm({ ...form, stock: Number(e.target.value) })} />
        <button disabled={submitting} className="col-span-5 bg-black text-white rounded py-2">
          {submitting ? "Creando..." : "Crear"}
        </button>
      </form>

      <ul className="divide-y rounded-2xl shadow">
        {items.map(p => (
          <li key={p.id} className="p-3 flex justify-between text-sm">
            <span className="font-mono">{p.sku}</span>
            <span className="flex-1 pl-3">{p.name}</span>
            <span>${p.price}</span>
            <span className="w-16 text-right">{p.stock}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
