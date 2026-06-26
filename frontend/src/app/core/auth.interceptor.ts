import { HttpErrorResponse, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, catchError, filter, switchMap, take, throwError } from 'rxjs';

import { ApiService } from './api.service';
import { TokenService } from './token.service';
import { environment } from '../../environments/environment';

let refreshing = false;
const refreshed$ = new BehaviorSubject<string | null>(null);

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE']);

function isApiRequest(url: string): boolean {
  const apiUrl = environment.apiUrl.replace(/\/$/, '');
  if (apiUrl.startsWith('/')) return url.startsWith(apiUrl);
  return url.startsWith(apiUrl) || url.startsWith('/api/');
}

function readCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;
  const match = document.cookie
    .split('; ')
    .find((row) => row.startsWith(`${encodeURIComponent(name)}=`));
  return match ? decodeURIComponent(match.split('=').slice(1).join('=')) : null;
}

function addAuth(req: HttpRequest<any>, access: string | null, guest: string): HttpRequest<any> {
  if (!isApiRequest(req.url)) return req;

  const headers: Record<string, string> = { 'X-Guest-Session': guest };
  if (access) headers['Authorization'] = `Bearer ${access}`;
  if (!SAFE_METHODS.has(req.method.toUpperCase()) && !req.headers.has('X-CSRFToken')) {
    const csrf = readCookie('csrftoken');
    if (csrf) headers['X-CSRFToken'] = csrf;
  }
  return req.clone({ setHeaders: headers, withCredentials: true });
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokens = inject(TokenService);
  const api = inject(ApiService);
  const router = inject(Router);

  const authedReq = addAuth(req, tokens.access, tokens.guestSession);

  return next(authedReq).pipe(
    catchError((err: HttpErrorResponse) => {
      if (!isApiRequest(req.url) || err.status !== 401 || !tokens.refresh) return throwError(() => err);
      if (req.url.includes('/auth/refresh/')) {
        tokens.clear();
        router.navigate(['/account/login']);
        return throwError(() => err);
      }
      return handle401(req, next, tokens, api);
    })
  );
};

function handle401(
  req: HttpRequest<any>,
  next: HttpHandlerFn,
  tokens: TokenService,
  api: ApiService,
): Observable<any> {
  if (refreshing) {
    return refreshed$.pipe(
      filter((x) => x !== null),
      take(1),
      switchMap((access) => next(addAuth(req, access, tokens.guestSession))),
    );
  }
  refreshing = true;
  refreshed$.next(null);
  return api.post<{ access: string; refresh?: string }>('/auth/refresh/', { refresh: tokens.refresh }).pipe(
    switchMap((r) => {
      refreshing = false;
      const newRefresh = r.refresh ?? tokens.refresh!;
      tokens.setTokens(r.access, newRefresh);
      refreshed$.next(r.access);
      return next(addAuth(req, r.access, tokens.guestSession));
    }),
    catchError((e) => {
      refreshing = false;
      tokens.clear();
      return throwError(() => e);
    }),
  );
}
