import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { shareReplay, tap } from 'rxjs/operators';

import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = environment.apiUrl;
  private cache = new Map<string, { expires: number; stream: Observable<unknown> }>();

  private url(path: string): string {
    return `${this.base}${path.startsWith('/') ? path : '/' + path}`;
  }

  private params(params?: Record<string, any>): HttpParams {
    let httpParams = new HttpParams();
    if (params) {
      for (const k of Object.keys(params).sort()) {
        const v = params[k];
        if (v !== undefined && v !== null && v !== '') {
          httpParams = httpParams.set(k, String(v));
        }
      }
    }
    return httpParams;
  }

  private cacheKey(path: string, params?: Record<string, any>): string {
    const httpParams = this.params(params);
    const query = httpParams.toString();
    return query ? `${path}?${query}` : path;
  }

  get<T>(path: string, params?: Record<string, any>): Observable<T> {
    const httpParams = this.params(params);
    return this.http.get<T>(this.url(path), { params: httpParams });
  }

  getCached<T>(path: string, params?: Record<string, any>, ttlMs = 120_000): Observable<T> {
    const key = this.cacheKey(path, params);
    const now = Date.now();
    const hit = this.cache.get(key);

    if (hit && hit.expires > now) {
      return hit.stream as Observable<T>;
    }

    const stream = this.get<T>(path, params).pipe(
      tap({
        error: () => this.cache.delete(key),
      }),
      shareReplay({ bufferSize: 1, refCount: false }),
    );
    this.cache.set(key, { expires: now + ttlMs, stream });
    return stream;
  }

  clearCache(prefix?: string) {
    if (!prefix) {
      this.cache.clear();
      return;
    }
    for (const key of this.cache.keys()) {
      if (key.startsWith(prefix)) this.cache.delete(key);
    }
  }

  post<T>(path: string, body: any): Observable<T> { return this.http.post<T>(this.url(path), body); }
  patch<T>(path: string, body: any): Observable<T> { return this.http.patch<T>(this.url(path), body); }
  put<T>(path: string, body: any): Observable<T> { return this.http.put<T>(this.url(path), body); }
  delete<T>(path: string): Observable<T> { return this.http.delete<T>(this.url(path)); }
}
