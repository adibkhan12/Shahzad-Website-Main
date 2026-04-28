import {
  MissingTranslationHandler,
  MissingTranslationHandlerParams,
} from '@ngx-translate/core';

/**
 * Safe fallback for any translation lookup that can't be resolved.
 *
 * Non-destructive contract:
 *   - NEVER return an empty string. If we did, the UI would go blank during
 *     the brief window before translations arrive from HTTP, or permanently
 *     if a key genuinely is missing.
 *   - Always return readable text, either the key itself or a humanised form
 *     of its last segment (e.g. "home.heroTitle1" → "Hero Title 1").
 *   - Warn once per missing key to the console so devs can find gaps without
 *     log spam.
 *
 * The pipe in ngx-translate v17 is impure and subscribes to onTranslationChange
 * and onLangChange — once the JSON loads, the pipe re-evaluates and paints
 * the real translated value over whatever fallback this handler returned.
 */
export class PrettyMissingTranslationHandler implements MissingTranslationHandler {
  private static warned = new Set<string>();

  handle(params: MissingTranslationHandlerParams): string {
    const key = params?.key ?? '';
    if (!key) return '';

    if (!PrettyMissingTranslationHandler.warned.has(key)) {
      PrettyMissingTranslationHandler.warned.add(key);
      console.warn(`[i18n] missing translation for key: "${key}"`);
    }

    // Always return readable text — never empty.
    return humanize(key);
  }
}

/**
 * "home.heroTitle1" → "Hero Title 1"
 * "nav.shop"        → "Shop"
 * "snake_case_key"  → "Snake Case Key"
 */
function humanize(key: string): string {
  const last = key.split('.').pop() || key;
  const spaced = last
    .replace(/([A-Z])/g, ' $1')
    .replace(/[_-]+/g, ' ')
    .replace(/(\d+)/g, ' $1')
    .replace(/\s+/g, ' ')
    .trim();
  const titled = spaced.replace(/\b\w/g, (c) => c.toUpperCase());
  // Fallback of last resort: return the raw key so nothing is ever invisible.
  return titled || key;
}
