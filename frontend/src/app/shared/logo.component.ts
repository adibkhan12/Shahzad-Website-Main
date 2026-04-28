import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

type Variant = 'badge' | 'mark' | 'lockup' | 'wordmark';

/**
 * Shahzad Mobile — tech-forward logo system.
 *
 * Palette:
 *   Deep navy #0B1426 → #0F2139 (body)
 *   Electric cyan #00D4FF / Sky #38BDF8 (accent gradient)
 *   Silver #E2E8F0 (monogram strokes on dark)
 *   Ink (currentColor) for mono variants — flips with light/dark theme.
 *
 * Variants:
 *   'badge'    — navy rounded-square with silver SM + cyan signal pad (favicon, app icon)
 *   'mark'     — outline SM with chip-pad terminals, inherits currentColor
 *   'lockup'   — badge + wordmark + tagline (headers)
 *   'wordmark' — text + cyan signal bar (letterhead, receipts)
 *
 * Usage:
 *   <app-logo variant="lockup" [size]="40" />
 *   <app-logo variant="mark" [size]="24" />
 */
@Component({
  selector: 'app-logo',
  standalone: true,
  imports: [CommonModule],
  template: `
    <!-- BADGE: chip-core icon for favicons & app tiles -->
    <svg *ngIf="variant === 'badge'" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 64 64" [style.width.px]="size" [style.height.px]="size"
         role="img" aria-label="Shahzad Mobile" class="block shrink-0">
      <defs>
        <!-- Beveled-square silhouette, reused as clip for the inner glow rim -->
        <clipPath [attr.id]="'b-clip-' + uid">
          <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"/>
        </clipPath>
        <!-- Faint chip-substrate dot grid -->
        <pattern [attr.id]="'b-grid-' + uid" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2" r="0.35" fill="#1E3A5F" opacity="0.55"/>
        </pattern>
        <!-- Soft cyan radial glow from the core -->
        <radialGradient [attr.id]="'b-core-' + uid" cx="0.5" cy="0.5" r="0.62">
          <stop offset="0%"   stop-color="#0EA5E9" stop-opacity="0.22"/>
          <stop offset="55%"  stop-color="#0EA5E9" stop-opacity="0.06"/>
          <stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/>
        </radialGradient>
        <linearGradient [attr.id]="'b-cy-' + uid" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%"   stop-color="#38BDF8"/>
          <stop offset="100%" stop-color="#00D4FF"/>
        </linearGradient>
        <!-- Gaussian blur for the inner-edge rim + trace soft-glow -->
        <filter [attr.id]="'b-blur-' + uid" x="-15%" y="-15%" width="130%" height="130%">
          <feGaussianBlur stdDeviation="1.6"/>
        </filter>
      </defs>

      <!-- Matte-black body, beveled square -->
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
            fill="#0A0A0A"/>
      <!-- Faint grid texture -->
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
            [attr.fill]="'url(#b-grid-' + uid + ')'"/>
      <!-- Lit-core radial glow from inside -->
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
            [attr.fill]="'url(#b-core-' + uid + ')'"/>

      <!-- Inner-edge rim glow: blurred cyan stroke, clipped so glow stays inside -->
      <g [attr.clip-path]="'url(#b-clip-' + uid + ')'">
        <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
              fill="none" [attr.stroke]="'url(#b-cy-' + uid + ')'"
              stroke-width="2.6" opacity="0.7"
              [attr.filter]="'url(#b-blur-' + uid + ')'"/>
      </g>

      <!-- Integrated cyan trace flowing through the M (behind the monogram).
           Enters from outside-left, crosses the M's body, exits right.
           Blurred copy sits beneath for the signal-glow feel. -->
      <g [attr.clip-path]="'url(#b-clip-' + uid + ')'">
        <line x1="26" y1="38" x2="62" y2="38"
              [attr.stroke]="'url(#b-cy-' + uid + ')'"
              stroke-width="2.2" opacity="0.45"
              [attr.filter]="'url(#b-blur-' + uid + ')'"/>
        <line x1="26" y1="38" x2="62" y2="38"
              [attr.stroke]="'url(#b-cy-' + uid + ')'"
              stroke-width="0.9" stroke-linecap="round"/>
      </g>

      <!-- SM monogram, uniform geometric strokes -->
      <g fill="none" stroke="#E2E8F0" stroke-width="3.6"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M 28 14 L 10 14 L 10 30 L 28 30 L 28 46 L 10 46"/>
        <path d="M 34 46 L 34 14 L 44 30 L 54 14 L 54 46"/>
      </g>

      <!-- Node dots at key junctions only: M valley + 2 trace vias on the M -->
      <circle cx="44" cy="30" r="1.5" [attr.fill]="'url(#b-cy-' + uid + ')'"/>
      <circle cx="34" cy="38" r="1.8" fill="#0A0A0A"
              [attr.stroke]="'url(#b-cy-' + uid + ')'" stroke-width="0.9"/>
      <circle cx="54" cy="38" r="1.8" fill="#0A0A0A"
              [attr.stroke]="'url(#b-cy-' + uid + ')'" stroke-width="0.9"/>
    </svg>

    <!-- MARK: outline SM with chip-pad terminals, theme-reactive -->
    <svg *ngIf="variant === 'mark'" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 64 64" [style.width.px]="size" [style.height.px]="size"
         role="img" aria-label="Shahzad Mobile" class="block shrink-0">
      <g fill="none" stroke="currentColor" stroke-width="4.25"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M 28 14 L 10 14 L 10 30 L 28 30 L 28 46 L 10 46"/>
        <path d="M 34 46 L 34 14 L 44 30 L 54 14 L 54 46"/>
      </g>
      <!-- Chip-pad terminal dots at open ends — tech nod, minimal -->
      <g fill="currentColor">
        <circle cx="28" cy="14" r="1.6"/>
        <circle cx="28" cy="46" r="1.6"/>
        <circle cx="10" cy="46" r="1.6"/>
        <circle cx="34" cy="46" r="1.6"/>
        <circle cx="54" cy="46" r="1.6"/>
      </g>
    </svg>

    <!-- LOCKUP: chip-core badge + wordmark + tagline — used in headers -->
    <svg *ngIf="variant === 'lockup'" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 340 64" [style.height.px]="size"
         role="img" aria-label="Shahzad Mobile" class="block shrink-0"
         preserveAspectRatio="xMinYMid meet">
      <defs>
        <clipPath [attr.id]="'l-clip-' + uid">
          <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"/>
        </clipPath>
        <pattern [attr.id]="'l-grid-' + uid" x="0" y="0" width="4" height="4" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2" r="0.35" fill="#1E3A5F" opacity="0.55"/>
        </pattern>
        <radialGradient [attr.id]="'l-core-' + uid" cx="0.5" cy="0.5" r="0.62">
          <stop offset="0%"   stop-color="#0EA5E9" stop-opacity="0.22"/>
          <stop offset="55%"  stop-color="#0EA5E9" stop-opacity="0.06"/>
          <stop offset="100%" stop-color="#0EA5E9" stop-opacity="0"/>
        </radialGradient>
        <linearGradient [attr.id]="'l-cy-' + uid" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%"   stop-color="#38BDF8"/>
          <stop offset="100%" stop-color="#00D4FF"/>
        </linearGradient>
        <filter [attr.id]="'l-blur-' + uid" x="-15%" y="-15%" width="130%" height="130%">
          <feGaussianBlur stdDeviation="1.6"/>
        </filter>
      </defs>

      <!-- Chip-core badge -->
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z" fill="#0A0A0A"/>
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
            [attr.fill]="'url(#l-grid-' + uid + ')'"/>
      <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
            [attr.fill]="'url(#l-core-' + uid + ')'"/>
      <g [attr.clip-path]="'url(#l-clip-' + uid + ')'">
        <path d="M 6 0 L 58 0 L 64 6 L 64 58 L 58 64 L 6 64 L 0 58 L 0 6 Z"
              fill="none" [attr.stroke]="'url(#l-cy-' + uid + ')'"
              stroke-width="2.6" opacity="0.7"
              [attr.filter]="'url(#l-blur-' + uid + ')'"/>
        <line x1="26" y1="38" x2="62" y2="38"
              [attr.stroke]="'url(#l-cy-' + uid + ')'"
              stroke-width="2.2" opacity="0.45"
              [attr.filter]="'url(#l-blur-' + uid + ')'"/>
        <line x1="26" y1="38" x2="62" y2="38"
              [attr.stroke]="'url(#l-cy-' + uid + ')'"
              stroke-width="0.9" stroke-linecap="round"/>
      </g>
      <g fill="none" stroke="#E2E8F0" stroke-width="3.6"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M 28 14 L 10 14 L 10 30 L 28 30 L 28 46 L 10 46"/>
        <path d="M 34 46 L 34 14 L 44 30 L 54 14 L 54 46"/>
      </g>
      <circle cx="44" cy="30" r="1.5" [attr.fill]="'url(#l-cy-' + uid + ')'"/>
      <circle cx="34" cy="38" r="1.8" fill="#0A0A0A"
              [attr.stroke]="'url(#l-cy-' + uid + ')'" stroke-width="0.9"/>
      <circle cx="54" cy="38" r="1.8" fill="#0A0A0A"
              [attr.stroke]="'url(#l-cy-' + uid + ')'" stroke-width="0.9"/>

      <!-- Wordmark: tight-tracked SHAHZAD, Inter bold -->
      <g transform="translate(82, 0)" fill="currentColor">
        <text x="0" y="28"
              font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
              font-weight="700" font-size="23" letter-spacing="0.5"
              dominant-baseline="central">SHAHZAD</text>
        <!-- Cyan signal bar under wordmark — the electronics cue -->
        <rect x="0" y="39" width="30" height="1.5" rx="0.75"
              [attr.fill]="'url(#l-cy-' + uid + ')'"/>
        <rect x="32" y="39.25" width="2" height="1" rx="0.5"
              [attr.fill]="'url(#l-cy-' + uid + ')'" opacity="0.7"/>
        <rect x="35" y="39.25" width="6" height="1" rx="0.5"
              [attr.fill]="'url(#l-cy-' + uid + ')'" opacity="0.45"/>
        <!-- Tagline: spaced small caps, muted -->
        <text x="0" y="52"
              font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
              font-weight="500" font-size="9" letter-spacing="2.8"
              dominant-baseline="central" opacity="0.62">MOBILE &amp; ELECTRONICS</text>
      </g>
    </svg>

    <!-- WORDMARK: text + cyan signal accent, no badge -->
    <svg *ngIf="variant === 'wordmark'" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 260 56" [style.height.px]="size"
         role="img" aria-label="Shahzad Mobile" class="block shrink-0"
         preserveAspectRatio="xMinYMid meet">
      <defs>
        <linearGradient [attr.id]="'w-cy-' + uid" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%"   stop-color="#38BDF8"/>
          <stop offset="100%" stop-color="#00D4FF"/>
        </linearGradient>
      </defs>
      <g fill="currentColor">
        <text x="0" y="22"
              font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
              font-weight="700" font-size="26" letter-spacing="0.6"
              dominant-baseline="central">SHAHZAD</text>
        <text x="0" y="46"
              font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
              font-weight="500" font-size="10" letter-spacing="3"
              dominant-baseline="central" opacity="0.62">MOBILE &amp; ELECTRONICS</text>
      </g>
      <!-- Cyan signal bar accent, top-right — chip trace motif -->
      <rect x="0" y="32" width="36" height="1.6" rx="0.8"
            [attr.fill]="'url(#w-cy-' + uid + ')'"/>
      <rect x="38" y="32.2" width="3" height="1.2" rx="0.6"
            [attr.fill]="'url(#w-cy-' + uid + ')'" opacity="0.65"/>
      <rect x="42.5" y="32.2" width="8" height="1.2" rx="0.6"
            [attr.fill]="'url(#w-cy-' + uid + ')'" opacity="0.4"/>
    </svg>
  `,
})
export class LogoComponent {
  @Input() variant: Variant = 'lockup';
  @Input() size = 32;

  /** Unique gradient-id suffix — prevents collisions when the same variant
   *  is rendered multiple times on one page. */
  readonly uid = Math.random().toString(36).slice(2, 8);
}
