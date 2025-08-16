import 'axios';

declare module 'axios' {
  // banderita interna que usamos en el interceptor
  export interface InternalAxiosRequestConfig<D = any> {
    _retry?: boolean;
  }
}
