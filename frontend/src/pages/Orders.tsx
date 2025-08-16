import { useEffect, useState } from "react";
import api from "../lib/api";
type Customer={id:number;name:string}; type Product={id:number;name:string;price:string;stock:number};
type Order={id:number;status:string;total:string};

export default function Orders(){
  const [customers,setC]=useState<Customer[]>([]);
  const [products,setP]=useState<Product[]>([]);
  const [order,setO]=useState<Order|null>(null);
  const [customerId,setCid]=useState<number|"">(""); const [productId,setPid]=useState<number|"">(""); const [qty,setQ]=useState(1);

  useEffect(()=>{(async()=>{
    const [c,p]=await Promise.all([api.get("/customers/"),api.get("/products/")]);
    setC(c.data.results??c.data); setP(p.data.results??p.data);
  })();},[]);

  async function createOrder(){ if(!customerId) return;
    const {data}=await api.post("/orders/",{customer:customerId,status:"draft",total:"0"}); setO(data); }
  async function addItem(){ if(!order||!productId||qty<=0) return;
    const prod=products.find(x=>x.id===productId)!;
    await api.post("/order-items/",{order:order.id,product:productId,quantity:qty,unit_price:prod.price,line_total:String(Number(prod.price)*qty)});
  }
  async function confirm(){ if(!order) return;
    const {data}=await api.post(`/orders/${order.id}/confirm/`); setO({...order,status:data.status,total:data.total}); }

  return (<div style={{padding:24}}>
    <h1>Órdenes</h1>
    {!order && (<div>
      <select value={customerId} onChange={e=>setCid(Number(e.target.value))}>
        <option value="">Selecciona cliente</option>
        {customers.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}
      </select>
      <button onClick={createOrder} disabled={!customerId}>Crear</button>
    </div>)}
    {order && (<div>
      <p>Orden #{order.id} | {order.status} | Total: {order.total||"0"}</p>
      <select value={productId} onChange={e=>setPid(Number(e.target.value))}>
        <option value="">Producto</option>
        {products.map(p=><option key={p.id} value={p.id}>{p.name} (${p.price}) stock:{p.stock}</option>)}
      </select>
      <input type="number" min={1} value={qty} onChange={e=>setQ(Number(e.target.value))}/>
      <button onClick={addItem}>Agregar ítem</button>
      <button onClick={confirm}>Confirmar</button>
    </div>)}
  </div>);
}
