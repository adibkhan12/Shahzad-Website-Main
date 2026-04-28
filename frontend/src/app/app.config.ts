import { provideHttpClient, withInterceptors } from '@angular/common/http';
import {
  APP_INITIALIZER,
  ApplicationConfig,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import {
  TranslateService,
  provideMissingTranslationHandler,
  provideTranslateService,
} from '@ngx-translate/core';
import { provideTranslateHttpLoader } from '@ngx-translate/http-loader';
import { firstValueFrom } from 'rxjs';

import { routes } from './app.routes';
import { authInterceptor } from './core/auth.interceptor';
import { languageInterceptor } from './core/language.interceptor';
import { PrettyMissingTranslationHandler } from './core/missing-translation.handler';

/**
 * App initialiser that BLOCKS Angular bootstrap until the initial JSON is
 * loaded into the TranslateStore. Without this, components render once
 * against an empty store (pipes fire, fall back to humanised keys), then
 * again after the HTTP completes — but the TranslatePipe caches its first
 * result per key, so the humanised fallback gets stuck in the DOM on every
 * key that happened to render during that race window.
 *
 * Choosing the initial lang:
 *   1. localStorage preference (what LanguageService will later persist)
 *   2. Browser locale starts with "ar" → "ar"
 *   3. Fallback → "en"
 *
 * We also always preload EN when starting in AR, because EN is the fallback
 * chain — any key missing in ar.json silently resolves from en.json.
 */
/**
 * APP_INITIALIZER factory — returns a function that Angular awaits before
 * finishing bootstrap. While that promise is pending, no component renders,
 * so there's no first-render race where pipes evaluate against an empty
 * TranslateStore and cache humanised fallbacks.
 */
function initTranslationsFactory(t: TranslateService): () => Promise<void> {
  return () => {
    const stored = (() => {
      try { return localStorage.getItem('shahzad_lang_v1'); }
      catch { return null; }
    })();
    const fromBrowser = (navigator?.language ?? 'en').toLowerCase().startsWith('ar') ? 'ar' : 'en';
    const initial = (stored === 'ar' || stored === 'en') ? stored : fromBrowser;

    t.addLangs(['en', 'ar']);
    t.setFallbackLang('en');

    // Reflect the chosen lang on <html> before the first render so CSS and
    // RTL kick in immediately with no flash.
    document.documentElement.setAttribute('lang', initial);
    document.documentElement.setAttribute('dir', initial === 'ar' ? 'rtl' : 'ltr');

    // Always wait for EN (it's the fallback chain) AND the initial lang.
    const needs: Array<Promise<unknown>> = [firstValueFrom(t.use('en'))];
    if (initial !== 'en') needs.push(firstValueFrom(t.use(initial)));
    return Promise.all(needs).then(() => void 0);
  };
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes, withInMemoryScrolling({ scrollPositionRestoration: 'top', anchorScrolling: 'enabled' })),
    provideHttpClient(withInterceptors([authInterceptor, languageInterceptor])),
    // ORDER MATTERS: provideTranslateService() registers a NoOpLoader when no
    // loader is in its config, which would override a HTTP loader registered
    // BEFORE it. So register the service first, then overwrite the loader
    // binding with the HTTP loader.
    provideTranslateService({
      lang: 'en',
      fallbackLang: 'en',
    }),
    // Loads /i18n/{en,ar}.json at runtime from the public/ folder.
    provideTranslateHttpLoader({
      prefix: '/i18n/',
      suffix: '.json',
      enforceLoading: true,
    }),
    provideMissingTranslationHandler(PrettyMissingTranslationHandler),
    // Block bootstrap until translations are in the store. This eliminates
    // the first-render race that was leaving humanised-key fallbacks stuck
    // on header/footer/home text for anything that rendered too early.
    {
      provide: APP_INITIALIZER,
      useFactory: initTranslationsFactory,
      deps: [TranslateService],
      multi: true,
    },
  ],
};
