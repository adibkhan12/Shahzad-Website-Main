import { Injectable, computed, inject, signal } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

export type AppLang = 'en' | 'ar';

/**
 * App locale owner — manages the active language, the <html> dir/lang
 * attributes, and localStorage persistence.
 *
 * Idiomatic ngx-translate v17 pattern:
 *   1. addLangs(['en','ar'])  — register known languages
 *   2. setFallbackLang('en')  — fallback chain for missing keys
 *   3. t.use(lang).subscribe() — kicks off the HTTP loader for that JSON
 *   4. subscribe to t.onLangChange for the "loaded + applied" signal.
 *      onLangChange is the authoritative confirmation that translations
 *      are in the store — we flip <html dir> + emit the signal from here,
 *      so UI only ever reflects real-loaded content, not a pending state.
 *
 * Diagnostics: every load logs a [i18n] line to the console with the lang
 * and key count. If you see keys missing, check the browser console first.
 */
@Injectable({ providedIn: 'root' })
export class LanguageService {
  private t = inject(TranslateService);
  private static readonly KEY = 'shahzad_lang_v1';
  private static readonly SUPPORTED: AppLang[] = ['en', 'ar'];

  readonly current = signal<AppLang>('en');
  readonly isRTL = computed(() => this.current() === 'ar');

  /**
   * Called once from AppComponent.ngOnInit. By the time this runs, the
   * APP_INITIALIZER in app.config.ts has already awaited the initial
   * translation JSON load — so the store is populated and the current
   * lang is set. Our job here is only to:
   *   - Sync our `current` signal to whatever the service decided
   *   - Subscribe to onLangChange so future flips update signal + dir
   *   - Log diagnostics for observability
   */
  init(): void {
    if (typeof window === 'undefined') return;

    // Reflect the already-loaded lang into our signal.
    const curr = (this.t.getCurrentLang() as AppLang) || 'en';
    this.current.set(curr);
    this.applyDirection(curr);

    // Future lang flips: sync signal + <html dir/lang>.
    this.t.onLangChange.subscribe((e) => {
      const lang = e.lang as AppLang;
      this.current.set(lang);
      this.applyDirection(lang);
      // eslint-disable-next-line no-console
      console.info(`[i18n] active language is now "${lang}"`);
    });
  }

  /** Switch to `lang` and persist the choice. Fires an HTTP load if the
   *  JSON for that lang hasn't been cached in the TranslateStore yet. */
  use(lang: AppLang): void {
    if (!LanguageService.SUPPORTED.includes(lang)) return;
    this.t.use(lang).subscribe({
      error: (err) => {
        console.error(`[i18n] failed to load "${lang}"`, err);
      },
    });
    this.persist(lang);
  }

  toggle(): void {
    this.use(this.current() === 'en' ? 'ar' : 'en');
  }

  // ── internals ─────────────────────────────────────────────────

  private applyDirection(lang: AppLang) {
    const html = document.documentElement;
    html.setAttribute('lang', lang);
    html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
  }

  private persist(lang: AppLang) {
    try { localStorage.setItem(LanguageService.KEY, lang); } catch { /* quota */ }
  }
}
