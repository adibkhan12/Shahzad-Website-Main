import { CommonModule } from '@angular/common';
import { Component, Input, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';
import { Product } from '../core/models';
import { WishlistService } from '../core/wishlist.service';

/**
 * Self-contained wishlist heart with WhatsApp-style reaction micro-interactions.
 *
 * Interaction layers:
 *   HOVER   — scale 1→1.1 + soft pink pulse ring (infinite, 1.6s, smooth ease).
 *   ADD     — heart pops scale 1→0.75→1.35→1 with spring overshoot; fills with a
 *             pink→rose gradient; six sparkle particles burst radially and fade;
 *             a central 4-point spark blooms then fades over ~900ms.
 *   REMOVE  — subtle shrink (1→0.82→1), fill fades back to outline. No particles.
 *   PENDING — button stays clickable visually; cursor turns progress. Spam clicks
 *             are absorbed by the WishlistService's pending-lock set.
 *
 * Event isolation: preventDefault + stopPropagation + stopImmediatePropagation.
 * Parent elements (anchors, routerLink, card containers) never see the click.
 *
 * Guest behaviour: renders identically but clicking routes to /account/login
 * with `next=<current URL>` so the user lands back where they were.
 *
 * Inputs:
 *   product — required. The full Product so the optimistic insert has data.
 *   size    — pixel diameter of the circle. Default 36.
 *   overlay — set as an attribute (e.g. `overlay`) to position absolutely
 *             top-right inside a `position: relative` parent.
 */
@Component({
  selector: 'app-wishlist-heart',
  standalone: true,
  imports: [CommonModule],
  template: `
    <button type="button"
            (click)="onClick($event)"
            [disabled]="disabled()"
            [attr.aria-label]="label()"
            [attr.aria-pressed]="favorited()"
            [class.is-fav]="favorited()"
            [class.is-adding]="phase() === 'adding'"
            [class.is-removing]="phase() === 'removing'"
            [style.width.px]="size"
            [style.height.px]="size"
            class="wish-btn">
      <svg class="heart-svg" viewBox="0 0 24 24"
           [attr.width]="iconSize" [attr.height]="iconSize">
        <defs>
          <linearGradient [attr.id]="gradId" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%"   stop-color="#f472b6"/>
            <stop offset="55%"  stop-color="#ec4899"/>
            <stop offset="100%" stop-color="#e11d48"/>
          </linearGradient>
        </defs>
        <path class="heart-path"
              d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
              [attr.fill]="favorited() ? gradUrl : 'none'"
              [attr.stroke]="favorited() ? 'none' : 'currentColor'"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"/>
      </svg>

      <!-- Burst layer: only rendered on ADD. Absolutely positioned so it
           can spill outside the button without reflowing layout. -->
      <span *ngIf="burst()" class="burst" aria-hidden="true">
        <span class="dot p1"></span>
        <span class="dot p2"></span>
        <span class="dot p3"></span>
        <span class="dot p4"></span>
        <span class="dot p5"></span>
        <span class="dot p6"></span>
        <svg class="spark" viewBox="0 0 24 24" aria-hidden="true">
          <!-- 4-point sparkle (star-burst): two crossed teardrop shapes -->
          <path d="M12 2 L13.2 10.2 L22 12 L13.2 13.8 L12 22 L10.8 13.8 L2 12 L10.8 10.2 Z"
                fill="currentColor"/>
        </svg>
      </span>
    </button>
  `,
  styles: [`
    :host { display: inline-flex; }
    :host([overlay]) {
      position: absolute;
      top: 0.75rem;
      right: 0.75rem;
      z-index: 20;
    }

    .wish-btn {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 9999px;
      border: 1px solid rgba(0,0,0,0.05);
      background: rgba(255,255,255,0.95);
      color: #0A0908;
      cursor: pointer;
      user-select: none;
      box-shadow: 0 4px 10px -2px rgba(0,0,0,0.08);
      transition:
        transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
        background-color 220ms cubic-bezier(0.22, 1, 0.36, 1),
        color 220ms cubic-bezier(0.22, 1, 0.36, 1),
        border-color 220ms ease,
        box-shadow 220ms ease;
    }
    .wish-btn:hover {
      color: #ec4899;
      background: #fff;
      border-color: rgba(236, 72, 153, 0.25);
      transform: scale(1.1);
      animation: wishHoverPulse 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    .wish-btn:active { transform: scale(0.94); }
    .wish-btn:disabled { cursor: progress; }

    /* HOVER PULSE ── soft expanding pink ring, infinite but subtle */
    @keyframes wishHoverPulse {
      0% {
        box-shadow:
          0 4px 10px -2px rgba(0,0,0,0.08),
          0 0 0 0 rgba(236, 72, 153, 0.45);
      }
      70% {
        box-shadow:
          0 4px 10px -2px rgba(0,0,0,0.08),
          0 0 0 12px rgba(236, 72, 153, 0);
      }
      100% {
        box-shadow:
          0 4px 10px -2px rgba(0,0,0,0.08),
          0 0 0 0 rgba(236, 72, 153, 0);
      }
    }

    /* FAVORITED STATE ── pink gradient fill + persistent glow */
    .wish-btn.is-fav {
      background: #fff0f6;
      border-color: rgba(236, 72, 153, 0.4);
      color: #ec4899;
      box-shadow: 0 6px 18px -4px rgba(236, 72, 153, 0.55);
    }
    .wish-btn.is-fav:hover {
      background: #ffe4ef;
      animation: wishHoverPulseFav 1.6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes wishHoverPulseFav {
      0%   { box-shadow: 0 6px 18px -4px rgba(236, 72, 153, 0.55),
                         0 0 0 0 rgba(236, 72, 153, 0.55); }
      70%  { box-shadow: 0 6px 18px -4px rgba(236, 72, 153, 0.55),
                         0 0 0 14px rgba(236, 72, 153, 0); }
      100% { box-shadow: 0 6px 18px -4px rgba(236, 72, 153, 0.55),
                         0 0 0 0 rgba(236, 72, 153, 0); }
    }

    /* HEART SVG ── smooth fill/outline transition */
    .heart-svg { display: block; }
    .heart-path {
      transition:
        fill 260ms cubic-bezier(0.22, 1, 0.36, 1),
        stroke 260ms ease;
    }

    /* ADD ── spring pop on the heart SVG */
    .wish-btn.is-adding .heart-svg {
      animation: heartAdd 560ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes heartAdd {
      0%   { transform: scale(1);    }
      30%  { transform: scale(0.72); }
      55%  { transform: scale(1.32); }
      75%  { transform: scale(0.96); }
      100% { transform: scale(1);    }
    }

    /* REMOVE ── gentle shrink, fill fades back to outline */
    .wish-btn.is-removing .heart-svg {
      animation: heartRemove 340ms cubic-bezier(0.33, 1, 0.68, 1);
    }
    @keyframes heartRemove {
      0%   { transform: scale(1);    opacity: 1;   }
      50%  { transform: scale(0.82); opacity: 0.55;}
      100% { transform: scale(1);    opacity: 1;   }
    }

    /* BURST LAYER ── sparkles + central star, visible only during add */
    .burst {
      position: absolute;
      inset: -8px;
      pointer-events: none;
      overflow: visible;
      z-index: 1;
    }
    .dot {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 7px;
      height: 7px;
      margin: -3.5px 0 0 -3.5px;
      border-radius: 50%;
      background: linear-gradient(135deg, #f472b6, #ec4899);
      opacity: 0;
      animation: particleFly 760ms cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    /* Six radial directions — biased slightly upward for a "happy burst" */
    .dot.p1 { --dx:  28px; --dy:  -6px; }
    .dot.p2 { --dx:  20px; --dy: -24px; animation-delay: 30ms; }
    .dot.p3 { --dx:   0px; --dy: -32px; animation-delay: 15ms; }
    .dot.p4 { --dx: -20px; --dy: -24px; animation-delay: 45ms; }
    .dot.p5 { --dx: -28px; --dy:  -6px; }
    .dot.p6 { --dx:   0px; --dy:  22px; width: 5px; height: 5px; animation-delay: 70ms; }

    @keyframes particleFly {
      0%   { transform: translate(0, 0) scale(0.5); opacity: 0; }
      15%  { opacity: 1; }
      100% { transform: translate(var(--dx, 0), var(--dy, 0)) scale(0.25) rotate(180deg); opacity: 0; }
    }

    /* SPARK ── central 4-point star that blooms and fades */
    .spark {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 22px;
      height: 22px;
      margin: -11px 0 0 -11px;
      color: #fbbf24;
      opacity: 0;
      animation: sparkBloom 900ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
      filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.55));
    }
    @keyframes sparkBloom {
      0%   { transform: scale(0.1) rotate(0deg);     opacity: 0;   }
      25%  { transform: scale(1.25) rotate(45deg);   opacity: 0.95;}
      60%  { transform: scale(1.05) rotate(120deg);  opacity: 0.6; }
      100% { transform: scale(1.45) rotate(220deg);  opacity: 0;   }
    }

    @media (prefers-reduced-motion: reduce) {
      .wish-btn,
      .wish-btn:hover,
      .wish-btn.is-fav:hover,
      .wish-btn.is-adding .heart-svg,
      .wish-btn.is-removing .heart-svg,
      .dot, .spark { animation: none !important; }
      .wish-btn:hover { transform: none; }
      .heart-path { transition: none; }
    }
  `],
})
export class WishlistHeartComponent {
  @Input({ required: true }) product!: Product;
  @Input() size = 36;
  @Input({ transform: (v: unknown) => v === '' || v === true || v === 'true' }) overlay = false;

  auth = inject(AuthService);
  wishlist = inject(WishlistService);
  private router = inject(Router);

  /** Animation phase: 'adding' on click-to-fav, 'removing' on click-to-unfav. */
  readonly phase = signal<'idle' | 'adding' | 'removing'>('idle');
  /** Burst layer is only rendered during an add — avoids rendering 7 elements
   *  on every card at rest. */
  readonly burst = signal(false);

  /** Unique SVG gradient id — prevents collisions when many hearts render. */
  readonly uid = Math.random().toString(36).slice(2, 8);

  readonly favorited = computed(() => this.wishlist.isFavorited(this.product.id));
  readonly disabled = computed(() => this.wishlist.isPending(this.product.id));

  get iconSize(): number { return Math.round(this.size * 0.44); }
  get gradId(): string { return `heart-grad-${this.uid}`; }
  get gradUrl(): string { return `url(#${this.gradId})`; }

  label = computed(() => {
    if (!this.auth.isAuthenticated()) return 'Sign in to save to wishlist';
    return this.favorited() ? 'Remove from wishlist' : 'Add to wishlist';
  });

  onClick(e: Event) {
    e.preventDefault();
    e.stopPropagation();
    if (typeof (e as any).stopImmediatePropagation === 'function') {
      (e as any).stopImmediatePropagation();
    }

    if (!this.auth.isAuthenticated()) {
      const returnUrl = this.router.url;
      this.router.navigate(['/account/login'], { queryParams: { next: returnUrl } });
      return;
    }

    const willBeFavorited = !this.favorited();
    this.phase.set(willBeFavorited ? 'adding' : 'removing');

    if (willBeFavorited) {
      // Re-trigger burst on rapid toggles: clear then re-enable next tick.
      this.burst.set(false);
      queueMicrotask(() => this.burst.set(true));
      setTimeout(() => this.burst.set(false), 900);
    }

    // Phase lasts through the longest animation; reset to 'idle' after.
    setTimeout(() => this.phase.set('idle'), 600);

    this.wishlist.toggle(this.product).subscribe();
  }
}
