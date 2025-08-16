import axios, { AxiosError, AxiosRequestConfig } from "axios";

// Add ImportMetaEnv declaration for Vite
interface ImportMetaEnv {
  readonly VITE_API_BASE?: string;
  // add other env variables here if needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

export type TokenPair = { access: string; refresh: string };

const baseURL = import.meta.env?.VITE_API_BASE ?? "/api";
const api = axios.create({ baseURL });

const getAccess = () => localStorage.getItem("access") || "";
const getRefresh = () => localStorage.getItem("refresh") || "";

export function setTokens(t?: Partial<TokenPair>) {
  if (!t) return;
  if (t.access) localStorage.setItem("access", t.access);
  if (t.refresh) localStorage.setItem("refresh", t.refresh);
}
export function loadTokens(): TokenPair | null {
  const access = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");
  return access && refresh ? { access, refresh } : null;
}
export function clearTokens() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

let refreshPromise: Promise<string> | null = null;
async function refreshAccess(): Promise<string> {
  if (!refreshPromise) {
    const refresh = getRefresh();
    refreshPromise = api
      .post("/auth/refresh/", { refresh })
      .then((r) => {
        const data = r.data as Partial<TokenPair>;
        if (data.access) localStorage.setItem("access", data.access);
        if (data.refresh) localStorage.setItem("refresh", data.refresh);
        return data.access || "";
      })
      .finally(() => {
        refreshPromise = null;
      });
  }
  return refreshPromise;
}

api.interceptors.request.use((config) => {
  const token = getAccess();
  if (token) {
    config.headers = config.headers || {};
    (config.headers as any).Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as AxiosRequestConfig & { _retry?: boolean };
    if (error.response?.status === 401 && !original?._retry) {
      original._retry = true;
      try {
        const newAccess = await refreshAccess();
        if (newAccess) {
          original.headers = original.headers || {};
          (original.headers as any).Authorization = `Bearer ${newAccess}`;
          return api.request(original);
        }
      } catch {
        clearTokens();
      }
    }
    return Promise.reject(error);
  }
);

export { api };
export default api;
