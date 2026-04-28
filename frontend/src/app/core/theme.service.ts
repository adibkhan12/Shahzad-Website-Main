import { DOCUMENT } from '@angular/common';
import { Injectable, inject, signal } from '@angular/core';

const KEY = 'sh_theme';
type Mode = 'light' | 'dark';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private doc = inject(DOCUMENT);
  readonly mode = signal<Mode>('dark');

  /** Initialise from localStorage or system preference (dark default). */
  init() {
    const saved = (localStorage.getItem(KEY) as Mode | null);
    const systemDark =
      typeof matchMedia !== 'undefined' &&
      matchMedia('(prefers-color-scheme: dark)').matches;
    const mode: Mode = saved ?? (systemDark ? 'dark' : 'dark'); // default dark
    this.apply(mode);
  }

  toggle() {
    this.apply(this.mode() === 'dark' ? 'light' : 'dark');
  }

  private apply(mode: Mode) {
    this.mode.set(mode);
    this.doc.documentElement.setAttribute('data-theme', mode);
    try { localStorage.setItem(KEY, mode); } catch {}
  }
}
