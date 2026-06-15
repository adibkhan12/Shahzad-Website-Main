import { Component, OnInit } from '@angular/core';

import { environment } from '../../environments/environment';

declare global {
  interface Window {
    Tawk_API?: any;
    Tawk_LoadStart?: Date;
  }
}

/**
 * Loads the Tawk.to live chat widget when both env vars are set.
 * Stays dormant otherwise — no script tag, no widget, nothing.
 *
 * Positioned at bottom-LEFT so it doesn't collide with the WhatsApp FAB
 * (which sits at bottom-right). Override in the Tawk.to dashboard if needed.
 */
@Component({
  selector: 'app-tawk-to',
  standalone: true,
  template: '',
})
export class TawkToComponent implements OnInit {
  private propertyId = environment.tawkToPropertyId;
  private widgetId = this.resolveWidgetId(environment.tawkToWidgetId);

  /**
   * Defensive: if a future contributor pastes the full embed URL into
   * `tawkToWidgetId` (e.g. `https://embed.tawk.to/{propId}/{widgetId}`),
   * pull just the last path segment so the script URL still ends up valid.
   */
  private resolveWidgetId(raw: string | undefined | null): string {
    const v = (raw || 'default').trim();
    if (v.startsWith('http')) {
      const last = v.split('/').filter(Boolean).pop();
      return last || 'default';
    }
    return v;
  }

  ngOnInit() {
    if (!this.propertyId) return;
    if (document.getElementById('tawk-script')) return; // already loaded

    window.Tawk_API = window.Tawk_API || {};
    window.Tawk_LoadStart = new Date();

    // Hide Tawk's default bubble — our `ChatLauncherComponent` is the single
    // entry point. The launcher re-shows + maximizes the widget on demand.
    window.Tawk_API.onLoad = function () {
      window.Tawk_API?.hideWidget?.();
    };

    // When the visitor closes/minimizes the chat, hide the bubble again so the
    // launcher stays the only visible entry point.
    window.Tawk_API.onChatMinimized = function () {
      window.Tawk_API?.hideWidget?.();
    };

    const s = document.createElement('script');
    s.id = 'tawk-script';
    s.async = true;
    s.src = `https://embed.tawk.to/${this.propertyId}/${this.widgetId}`;
    s.charset = 'UTF-8';
    s.setAttribute('crossorigin', '*');
    document.body.appendChild(s);
  }
}
