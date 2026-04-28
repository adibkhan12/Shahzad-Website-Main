import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;

  private url(path: string): string {
    return `${this.base}${path.startsWith('/') ? path : '/' + path}`;
  }

  get<T>(path: string, params?: Record<string, any>): Observable<T> {
    let httpParams = new HttpParams();
    if (params) {
      for (const k of Object.keys(params)) {
        const v = params[k];
        if (v !== undefined && v !== null && v !== '') {
          httpParams = httpParams.set(k, String(v));
        }
      }
    }
    return this.http.get<T>(this.url(path), { params: httpParams });
  }

  post<T>(path: string, body: any): Observable<T> { return this.http.post<T>(this.url(path), body); }
  patch<T>(path: string, body: any): Observable<T> { return this.http.patch<T>(this.url(path), body); }
  put<T>(path: string, body: any): Observable<T> { return this.http.put<T>(this.url(path), body); }
  delete<T>(path: string): Observable<T> { return this.http.delete<T>(this.url(path)); }
}
