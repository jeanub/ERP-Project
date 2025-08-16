import React, { createContext, useContext, useState } from "react";
import { api, setTokens, loadTokens, type TokenPair } from "../lib/api";

type AuthContextType = {
  tokens: TokenPair | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
};

const AuthCtx = createContext<AuthContextType>({
  tokens: null,
  login: async () => false,
  logout: () => {},
});

export const useAuth = () => useContext(AuthCtx);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [tokens, setTok] = useState<TokenPair | null>(loadTokens());

  const login = async (username: string, password: string) => {
  try {
    const { data } = await api.post("/auth/token/", { username, password });
    const pair = { access: data.access as string, refresh: data.refresh as string };
    setTokens(pair);
    setTok(pair);
    return true;
  } catch {
    return false;
  }
};


  const logout = () => {
    setTokens(null);
    setTok(null);
  };

  return (
    <AuthCtx.Provider value={{ tokens, login, logout }}>
      {children}
    </AuthCtx.Provider>
  );
};
