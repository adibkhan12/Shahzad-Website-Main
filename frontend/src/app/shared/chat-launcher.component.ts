import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';

import { environment } from '../../environments/environment';

declare global {
  interface Window {
    Tawk_API?: any;
  }
}

/**
 * Single floating chat launcher (bottom-right). When tapped, expands to show
 * available channels (WhatsApp, Tawk.to live chat). Replaces the previous
 * standalone WhatsApp FAB so the corner stays visually clean.
 *
 * Tawk.to's default bubble is suppressed by `TawkToComponent`; this launcher
 * triggers the Tawk panel via `Tawk_API.maximize()`.
 */
@Component({
  selector: 'app-chat-launcher',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- click-outside backdrop, only rendered when open -->
    <div *ngIf="open()" (click)="close()" class="fixed inset-0 z-40 cursor-default" aria-hidden="true"></div>

    <div class="fixed bottom-5 right-5 md:bottom-6 md:right-6 z-50 flex flex-col items-end gap-3">
      <!-- channel options stack -->
      <div
        class="flex flex-col items-end gap-2 transition-all duration-300 ease-smooth"
        [class.opacity-100]="open()"
        [class.translate-y-0]="open()"
        [class.pointer-events-auto]="open()"
        [class.opacity-0]="!open()"
        [class.translate-y-4]="!open()"
        [class.pointer-events-none]="!open()"
      >
        <!-- WhatsApp -->
        <a
          [href]="whatsappUrl"
          target="_blank"
          rel="noopener"
          (click)="close()"
          class="flex items-center gap-2.5 pl-3 pr-4 py-2 bg-[#25D366] text-white rounded-full shadow-lift hover:scale-[1.04] active:scale-100 transition-transform duration-200"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.194 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>
          </svg>
          <span class="text-sm font-medium whitespace-nowrap">WhatsApp</span>
        </a>

        <!-- Live chat (Tawk.to) -->
        <button
          *ngIf="tawkEnabled"
          type="button"
          (click)="openLiveChat()"
          class="flex items-center gap-2.5 pl-3 pr-4 py-2 bg-ink text-white rounded-full shadow-lift hover:scale-[1.04] active:scale-100 transition-transform duration-200"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          <span class="text-sm font-medium whitespace-nowrap">Live chat</span>
        </button>
      </div>

      <!-- main toggle button -->
      <button
        type="button"
        (click)="toggle()"
        [attr.aria-expanded]="open()"
        aria-label="Contact us"
        class="relative w-14 h-14 rounded-full text-white shadow-lift flex items-center justify-center transition-all duration-300 ease-smooth hover:scale-[1.05] active:scale-100"
        [class.bg-ink]="open()"
        [class.bg-brand-600]="!open()"
      >
        <!-- subtle ping when closed, no ping when open -->
        <span
          *ngIf="!open()"
          class="absolute inset-0 rounded-full bg-brand-600 opacity-30 animate-ping"
        ></span>
        <svg *ngIf="!open()" class="relative w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        <svg *ngIf="open()" class="relative w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
  `,
})
export class ChatLauncherComponent {
  open = signal(false);
  whatsappUrl =
    `https://wa.me/${environment.whatsappNumber}` +
    `?text=${encodeURIComponent('Hi, I have a question about a product.')}`;
  tawkEnabled = !!environment.tawkToPropertyId;

  toggle() {
    this.open.update((o) => !o);
  }

  close() {
    this.open.set(false);
  }

  openLiveChat() {
    this.close();
    // Tawk_API may not be ready yet if the user clicked very quickly after page load.
    // Best effort: try maximize, fall through silently otherwise.
    try {
      window.Tawk_API?.maximize?.();
    } catch {
      /* ignore */
    }
  }
}
