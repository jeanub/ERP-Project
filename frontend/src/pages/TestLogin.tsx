
import { useAuth } from "../auth/AuthProvider";
import { useState } from "react";
import api from "../lib/api"; 

export default function TestLogin() {
  const { login, tokens } = useAuth();
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");

  return (
    <div style={{ padding: 16 }}>
      <input value={user} onChange={e => setUser(e.target.value)} placeholder="Username" />
      <input type="password" value={pass} onChange={e => setPass(e.target.value)} placeholder="Password" />
      <button onClick={() => login(user, pass)}>Login</button>
      <pre>{JSON.stringify(tokens, null, 2)}</pre>
    </div>
  );
}
