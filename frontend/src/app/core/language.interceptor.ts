import { HttpInterceptorFn } from '@angular/common/http';

import { environment } from '../../environments/environment';

function isApiRequest(url: string): boolean {
  const apiUrl = environment.apiUrl.replace(/\/$/, '');
  if (apiUrl.startsWith('/')) return url.startsWith(apiUrl);
  return url.startsWith(apiUrl) || url.startsWith('/api/');
}

/**
 * Stamps every outgoing API request with `Accept-Language: <current>` so
 * the backend serializer can return localized content (e.g. ad banners).
 *
 * Read the active lang from `<html lang>` rather than injecting
 * LanguageService — the latter creates a circular DI when the interceptor
 * runs during the TranslateService's own APP_INITIALIZER HTTP load
 * (LanguageService → TranslateService → HttpClient → languageInterceptor →
 * LanguageService ⟲). The `<html lang>` attribute is set synchronously by
 * the initializer before any load kicks off, so it's authoritative and
 * cheap to read.
 *
 * We also explicitly skip the /i18n/ JSON fetches themselves — those are
 * static public files and don't need the header, and stamping them could
 * further muddy caching semantics.
 */
export const languageInterceptor: HttpInterceptorFn = (req, next) => {
  if (!isApiRequest(req.url)) return next(req);

  // Leave translation JSON fetches alone — they're language-agnostic statics.
  if (req.url.includes('/i18n/')) return next(req);

  // Respect any explicit header the caller already set.
  if (req.headers.has('Accept-Language')) return next(req);

  const lang =
    (typeof document !== 'undefined' && document.documentElement.getAttribute('lang')) || 'en';

  return next(req.clone({ setHeaders: { 'Accept-Language': lang } }));
};
