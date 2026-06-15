import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

type Stage = 'teaser' | 'rising' | 'idle' | 'flipping' | 'flipped' | 'zooming' | 'done';

/**
 * First-visit cinematic — five stages:
 *   1. teaser  — "Experience Shahzad Tech" + big "Click to Explore" CTA.
 *                No phone visible yet; the user has a clear affordance to act.
 *   2. rising  — the phone swoops up from below the viewport into place.
 *   3. idle    — phone floats in 3D back-pose; a cyan halo makes it pop
 *                against the dark scene. Hint: "Tap to turn it over".
 *   4. flipping/flipped — device rotates and the on-screen Shahzad preview
 *                fades in on its display.
 *   5. zooming — phone zooms into the viewport; the real home page reveals.
 *
 * Auto-skips on return visits (sessionStorage) or when reduced motion is on.
 */
@Component({
  selector: 'app-intro-showcase',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="stage() !== 'done'" class="intro-root" [attr.data-stage]="stage()" (click)="onTap()">
      <div class="intro-bg"></div>
      <div class="intro-glow intro-glow-a"></div>
      <div class="intro-glow intro-glow-b"></div>

      <button class="intro-skip" (click)="skip($event)" aria-label="Skip intro">
        Skip intro →
      </button>

      <!-- Stage 1: teaser — big headline + CTA so the user knows what's coming. -->
      <div class="intro-teaser" [class.visible]="stage() === 'teaser'" (click)="onTap()">
        <span class="teaser-eyebrow">Welcome</span>
        <h1 class="teaser-title display">
          Experience <em>Shahzad Tech</em>
        </h1>
        <p class="teaser-sub">A quick look at what awaits you inside.</p>
        <button type="button" class="teaser-cta" (click)="onTap(); $event.stopPropagation()">
          <span>Click to Explore</span>
          <svg class="teaser-arrow" viewBox="0 0 24 24" width="18" height="18" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 5v14M19 12l-7 7-7-7"/>
          </svg>
        </button>
      </div>

      <!-- Stage 3+: hint labels appear above the phone once it has risen. -->
      <div class="intro-label" [class.visible]="stage() === 'idle'">
        <span class="intro-eyebrow">Shahzad · Experience</span>
        <span class="intro-hint">Tap the device to turn it over</span>
      </div>

      <div class="intro-label" [class.visible]="stage() === 'flipped'">
        <span class="intro-eyebrow">Tap again</span>
        <span class="intro-hint">Step inside the store</span>
      </div>

      <div class="intro-scene">
        <div class="intro-phone-float" [attr.data-stage]="stage()">
          <div class="intro-phone" [attr.data-stage]="stage()">

            <!-- BACK of phone -->
            <div class="phone-face phone-back">
              <svg viewBox="0 0 300 620" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                <defs>
                  <!-- Titanium body: darker base with a bright metallic highlight
                       band running diagonally. Mimics a real brushed-aluminum
                       catch of light. -->
                  <linearGradient id="iph-body" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0"    stop-color="#3a3049"/>
                    <stop offset="0.18" stop-color="#1c1629"/>
                    <stop offset="0.5"  stop-color="#100b1c"/>
                    <stop offset="0.82" stop-color="#1e1830"/>
                    <stop offset="1"    stop-color="#0a0614"/>
                  </linearGradient>
                  <!-- Specular diagonal sweep — subtle, 8% opacity max -->
                  <linearGradient id="iph-sweep" x1="0" y1="0" x2="1" y2="1.3">
                    <stop offset="0"    stop-color="rgba(255,255,255,0.22)"/>
                    <stop offset="0.12" stop-color="rgba(255,255,255,0.02)"/>
                    <stop offset="0.6"  stop-color="rgba(255,255,255,0)"/>
                    <stop offset="0.88" stop-color="rgba(255,255,255,0.03)"/>
                    <stop offset="1"    stop-color="rgba(255,255,255,0.14)"/>
                  </linearGradient>
                  <!-- Lens glass: blue-violet sapphire with cold highlights -->
                  <radialGradient id="lens-glass" cx="0.35" cy="0.28" r="0.95">
                    <stop offset="0"    stop-color="#5a4580"/>
                    <stop offset="0.25" stop-color="#2a1e42"/>
                    <stop offset="0.6"  stop-color="#0a0618"/>
                    <stop offset="1"    stop-color="#020106"/>
                  </radialGradient>
                  <!-- Inner aperture darkness -->
                  <radialGradient id="lens-pupil" cx="0.5" cy="0.5" r="0.5">
                    <stop offset="0"    stop-color="#000"/>
                    <stop offset="0.7"  stop-color="#020108"/>
                    <stop offset="1"    stop-color="#080318"/>
                  </radialGradient>
                  <!-- Plateau — recessed, darker than body, subtle inner glow -->
                  <radialGradient id="plateau-shade" cx="0.45" cy="0.35" r="1">
                    <stop offset="0"    stop-color="#15101f"/>
                    <stop offset="1"    stop-color="#020106"/>
                  </radialGradient>
                  <!-- LED flash core -->
                  <radialGradient id="flash-core" cx="0.35" cy="0.35" r="0.7">
                    <stop offset="0"    stop-color="#ffffff"/>
                    <stop offset="0.45" stop-color="#e8dffc"/>
                    <stop offset="1"    stop-color="#7d6eac"/>
                  </radialGradient>
                </defs>

                <!-- Body -->
                <rect x="5" y="5" width="290" height="610" rx="48" ry="48" fill="url(#iph-body)"/>
                <rect x="5" y="5" width="290" height="610" rx="48" ry="48" fill="url(#iph-sweep)"/>
                <!-- Inner bezel: bright top-left rim (light catch) + dark bottom-right -->
                <rect x="5.5" y="5.5" width="289" height="609" rx="47.5" ry="47.5"
                      fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="0.8"/>
                <rect x="7" y="7" width="286" height="606" rx="46" ry="46"
                      fill="none" stroke="rgba(0,0,0,0.5)" stroke-width="1.2"/>

                <!-- Side buttons: with shadow + highlight for depth -->
                <g>
                  <rect x="2" y="150" width="3" height="38" rx="1.5" fill="#1a1426"/>
                  <rect x="2" y="150.5" width="3" height="1.5" rx="0.75" fill="rgba(255,255,255,0.18)"/>
                  <rect x="2" y="200" width="3" height="60" rx="1.5" fill="#1a1426"/>
                  <rect x="2" y="200.5" width="3" height="1.5" rx="0.75" fill="rgba(255,255,255,0.18)"/>
                  <rect x="295" y="180" width="3" height="84" rx="1.5" fill="#1a1426"/>
                  <rect x="295" y="180.5" width="3" height="1.5" rx="0.75" fill="rgba(255,255,255,0.18)"/>
                </g>

                <!-- Camera plateau: chamfered with bright outer ring + inset shadow -->
                <rect x="26" y="26" width="122" height="122" rx="30" ry="30"
                      fill="rgba(0,0,0,0.4)"/>
                <rect x="28" y="28" width="118" height="118" rx="28" ry="28"
                      fill="url(#plateau-shade)"/>
                <rect x="28" y="28" width="118" height="118" rx="28" ry="28"
                      fill="none" stroke="rgba(255,255,255,0.16)" stroke-width="0.8"/>
                <rect x="29.5" y="29.5" width="115" height="115" rx="26.5" ry="26.5"
                      fill="none" stroke="rgba(0,0,0,0.6)" stroke-width="1.5"/>

                <!-- Lens factory: 3 lenses in a triangle. Each has 6 layers:
                     ring bezel → chamfer → outer glass → mid aperture → pupil
                     → specular highlight → micro pinprick highlight -->
                <g>
                  <!-- TL lens -->
                  <g transform="translate(60 60)">
                    <circle r="23.5" fill="#000"/>
                    <circle r="22" fill="rgba(0,0,0,0.7)"/>
                    <circle r="22" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="0.6"/>
                    <circle r="19" fill="url(#lens-glass)"/>
                    <circle r="14" fill="url(#lens-pupil)"/>
                    <circle r="10" fill="#000"/>
                    <!-- Thin iris ring -->
                    <circle r="10.5" fill="none" stroke="rgba(80,60,110,0.6)" stroke-width="0.4"/>
                    <!-- Broad soft highlight -->
                    <ellipse cx="-5" cy="-5" rx="7" ry="5" fill="rgba(200,180,255,0.22)"/>
                    <!-- Crisp pinprick -->
                    <circle r="1.8" cx="-6.5" cy="-6.5" fill="rgba(255,245,255,0.9)"/>
                    <!-- Tiny secondary glint -->
                    <circle r="0.8" cx="4" cy="4" fill="rgba(220,200,255,0.45)"/>
                  </g>
                  <!-- BL lens -->
                  <g transform="translate(60 114)">
                    <circle r="23.5" fill="#000"/>
                    <circle r="22" fill="rgba(0,0,0,0.7)"/>
                    <circle r="22" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="0.6"/>
                    <circle r="19" fill="url(#lens-glass)"/>
                    <circle r="14" fill="url(#lens-pupil)"/>
                    <circle r="10" fill="#000"/>
                    <circle r="10.5" fill="none" stroke="rgba(80,60,110,0.6)" stroke-width="0.4"/>
                    <ellipse cx="-5" cy="-5" rx="7" ry="5" fill="rgba(200,180,255,0.22)"/>
                    <circle r="1.8" cx="-6.5" cy="-6.5" fill="rgba(255,245,255,0.9)"/>
                    <circle r="0.8" cx="4" cy="4" fill="rgba(220,200,255,0.45)"/>
                  </g>
                  <!-- Right lens -->
                  <g transform="translate(114 87)">
                    <circle r="23.5" fill="#000"/>
                    <circle r="22" fill="rgba(0,0,0,0.7)"/>
                    <circle r="22" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="0.6"/>
                    <circle r="19" fill="url(#lens-glass)"/>
                    <circle r="14" fill="url(#lens-pupil)"/>
                    <circle r="10" fill="#000"/>
                    <circle r="10.5" fill="none" stroke="rgba(80,60,110,0.6)" stroke-width="0.4"/>
                    <ellipse cx="-5" cy="-5" rx="7" ry="5" fill="rgba(200,180,255,0.22)"/>
                    <circle r="1.8" cx="-6.5" cy="-6.5" fill="rgba(255,245,255,0.9)"/>
                    <circle r="0.8" cx="4" cy="4" fill="rgba(220,200,255,0.45)"/>
                  </g>
                </g>

                <!-- Flash: bright warm-white core with halo -->
                <g transform="translate(175 58)">
                  <circle r="12" fill="rgba(0,0,0,0.5)"/>
                  <circle r="10" fill="#0a0612"/>
                  <circle r="10" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="0.5"/>
                  <circle r="6" fill="url(#flash-core)"/>
                  <circle r="2" cx="-1.5" cy="-1.5" fill="#ffffff"/>
                </g>
                <!-- LiDAR sensor: sapphire-tinted glass pit -->
                <g transform="translate(175 105)">
                  <circle r="12" fill="rgba(0,0,0,0.5)"/>
                  <circle r="10" fill="#070410"/>
                  <circle r="10" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="0.5"/>
                  <circle r="6" fill="#020106"/>
                  <circle r="4.5" fill="rgba(150,100,220,0.4)"/>
                  <circle r="1.8" cx="-1.5" cy="-1.5" fill="rgba(220,200,255,0.7)"/>
                </g>
                <!-- Mic hole -->
                <circle cx="175" cy="140" r="3" fill="rgba(0,0,0,0.9)"/>
                <circle cx="175" cy="140" r="3" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>

                <!-- Apple logo — polished chrome look -->
                <g transform="translate(127 300) scale(1.95)">
                  <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01z"
                        fill="rgba(255,255,255,0.32)"/>
                  <path d="M12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"
                        fill="rgba(255,255,255,0.32)"/>
                </g>

                <!-- iPhone wordmark -->
                <text x="150" y="560" text-anchor="middle"
                      font-family="Inter, system-ui, sans-serif"
                      font-size="10"
                      font-weight="300"
                      letter-spacing="2"
                      fill="rgba(255,255,255,0.28)">iPhone</text>
              </svg>
            </div>

            <!-- FRONT of phone: bezel + screen -->
            <div class="phone-face phone-front">
              <svg viewBox="0 0 300 620" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="phone-chassis">
                <defs>
                  <linearGradient id="iph-bezel" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0"    stop-color="#3a3049"/>
                    <stop offset="0.5"  stop-color="#120c1f"/>
                    <stop offset="1"    stop-color="#0a0614"/>
                  </linearGradient>
                  <linearGradient id="iph-frame" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0"    stop-color="rgba(255,255,255,0.18)"/>
                    <stop offset="1"    stop-color="rgba(255,255,255,0.02)"/>
                  </linearGradient>
                </defs>
                <!-- Outer body -->
                <rect x="5" y="5" width="290" height="610" rx="48" ry="48" fill="url(#iph-bezel)"/>
                <!-- Brushed titanium frame highlight -->
                <rect x="5.5" y="5.5" width="289" height="609" rx="47.5" ry="47.5"
                      fill="none" stroke="url(#iph-frame)" stroke-width="0.8"/>
                <!-- Inner bezel shadow -->
                <rect x="7" y="7" width="286" height="606" rx="46" ry="46"
                      fill="none" stroke="rgba(0,0,0,0.55)" stroke-width="1.2"/>
                <!-- Screen cavity -->
                <rect x="12" y="12" width="276" height="596" rx="42" ry="42" fill="#000"/>
                <!-- Thin silver inner stroke where glass meets frame -->
                <rect x="12.5" y="12.5" width="275" height="595" rx="41.5" ry="41.5"
                      fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.6"/>
              </svg>
              <!-- Screen glare: diagonal gloss stripe that catches light —
                   only over the screen area, not the bezel. -->
              <div class="phone-glare"></div>

              <div class="phone-screen">
                <div class="phone-dyn-island">
                  <span class="island-cam"></span>
                </div>
                <div class="screen-content">
                  <div class="mini-site">
                    <div class="mini-nav">
                      <span class="mini-logo">SHAHZAD</span>
                      <span class="mini-dots"><i></i><i></i><i></i></span>
                    </div>
                    <div class="mini-eyebrow">Pre-loved · Refurbished · Honest</div>
                    <h2 class="mini-title">Quality tech,<br/><em>priced honestly.</em></h2>
                    <p class="mini-sub">Sharjah's trusted specialist in second-hand &amp; refurbished devices.</p>
                    <div class="mini-btns">
                      <span class="mini-btn mini-btn-primary">Browse →</span>
                      <span class="mini-btn">Repairs</span>
                    </div>
                    <div class="mini-card">
                      <div class="mini-card-img"></div>
                      <div class="mini-card-body">
                        <div class="mini-card-title">iPhone 15 Pro</div>
                        <div class="mini-card-price">2,999 AED</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="phone-shadow"></div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    :host { display: contents; }

    .intro-root {
      position: fixed;
      inset: 0;
      z-index: 9999;
      overflow: hidden;
      cursor: pointer;
      perspective: 2200px;
      perspective-origin: 50% 42%;
      transition: opacity 700ms cubic-bezier(0.76, 0, 0.24, 1);
      /* Warm ivory — matches the site's design system (--c-bg) so when we
         fade out at the end of the zoom, there's no brightness flash. */
      background: #FAFAF7;
      user-select: none;
      color: #0A0908;
    }
    .intro-root[data-stage="zooming"] { cursor: default; }

    .intro-bg {
      position: absolute;
      inset: 0;
      /* Light premium wash: soft violet mist pooling top-centre, warm
         peach grounding bottom-left, ivory base. Keeps the showroom feel
         without going dark and heavy. */
      background:
        radial-gradient(ellipse 60% 50% at 50% 28%, rgba(139, 43, 219, 0.14) 0%, transparent 55%),
        radial-gradient(ellipse 70% 55% at 18% 85%, rgba(245, 215, 154, 0.32) 0%, transparent 60%),
        radial-gradient(ellipse 65% 50% at 90% 15%, rgba(180, 210, 240, 0.22) 0%, transparent 60%),
        linear-gradient(180deg, #FAFAF7 0%, #F4EEFB 100%);
    }

    .intro-glow {
      position: absolute;
      width: 55vmin;
      height: 55vmin;
      border-radius: 50%;
      filter: blur(90px);
      opacity: 0.6;
      pointer-events: none;
      animation: glowFloat 14s ease-in-out infinite;
    }
    .intro-glow-a {
      /* Lavender cloud */
      background: radial-gradient(circle, rgba(180, 120, 230, 0.45) 0%, transparent 65%);
      top: -8%; left: -12%;
    }
    .intro-glow-b {
      /* Warm peach cloud — the brand's warm-cool contrast */
      background: radial-gradient(circle, rgba(255, 200, 160, 0.38) 0%, transparent 65%);
      bottom: -14%; right: -10%;
      animation-delay: -7s;
    }
    @keyframes glowFloat {
      0%, 100% { transform: translate(0,0) scale(1); }
      50%      { transform: translate(5vmin,-3vmin) scale(1.15); }
    }

    .intro-skip {
      position: absolute;
      top: 28px;
      right: 28px;
      z-index: 5;
      padding: 10px 18px;
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(10, 9, 8, 0.6);
      background: rgba(255, 255, 255, 0.7);
      border: 1px solid rgba(10, 9, 8, 0.08);
      border-radius: 999px;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      cursor: pointer;
      transition: all 300ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    .intro-skip:hover {
      color: #0A0908;
      background: rgba(255, 255, 255, 0.95);
      border-color: rgba(10, 9, 8, 0.2);
    }

    /* Hints float above the phone — never over it — so the device stays uncluttered. */
    .intro-label {
      position: absolute;
      left: 50%;
      top: clamp(28px, 7vh, 80px);
      transform: translateX(-50%);
      text-align: center;
      color: #0A0908;
      opacity: 0;
      transition: opacity 600ms 400ms cubic-bezier(0.22, 1, 0.36, 1);
      pointer-events: none;
      z-index: 3;
      max-width: 90vw;
    }
    .intro-label.visible { opacity: 1; }
    .intro-eyebrow {
      display: block;
      font-size: 11px;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: #740DC2;
      margin-bottom: 10px;
    }
    .intro-hint {
      display: block;
      font-size: 15px;
      font-weight: 300;
      letter-spacing: 0.02em;
      color: rgba(10, 9, 8, 0.75);
      animation: pulseText 2.4s ease-in-out infinite;
    }
    @keyframes pulseText {
      0%, 100% { opacity: 0.55; }
      50%      { opacity: 1; }
    }

    /* ── Teaser stage (before the phone appears) ───────────────────── */
    .intro-teaser {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 0 24px;
      opacity: 0;
      pointer-events: none;
      transition:
        opacity 600ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 900ms cubic-bezier(0.76, 0, 0.24, 1);
      transform: translateY(0);
      z-index: 4;
      cursor: pointer;
    }
    .intro-teaser.visible {
      opacity: 1;
      pointer-events: auto;
    }
    /* When we leave the teaser stage, lift the headline up and fade it
       before the phone rises — so they never overlap visually. */
    .intro-root:not([data-stage="teaser"]) .intro-teaser {
      transform: translateY(-40px);
    }

    .teaser-eyebrow {
      display: block;
      font-size: 11px;
      letter-spacing: 0.32em;
      text-transform: uppercase;
      color: #740DC2;
      margin-bottom: 20px;
      opacity: 0;
      animation: teaserFadeIn 700ms 200ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
    .teaser-title {
      font-size: clamp(2.5rem, 7vw, 5rem);
      line-height: 1;
      letter-spacing: -0.02em;
      color: #0A0908;
      margin: 0 0 18px;
      max-width: 14ch;
      opacity: 0;
      animation: teaserFadeIn 900ms 350ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
    .teaser-title em {
      color: #740DC2;
      font-style: italic;
    }
    .teaser-sub {
      font-size: 15px;
      font-weight: 300;
      color: rgba(10, 9, 8, 0.6);
      margin: 0 0 36px;
      opacity: 0;
      animation: teaserFadeIn 700ms 550ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
    }
    .teaser-cta {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 14px 28px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #fff;
      background: linear-gradient(135deg, #8b2bdb 0%, #3d1766 100%);
      border: 1px solid rgba(201, 163, 255, 0.3);
      border-radius: 999px;
      cursor: pointer;
      box-shadow:
        0 10px 30px -8px rgba(139, 43, 219, 0.55),
        0 0 0 0 rgba(139, 43, 219, 0.35);
      transition:
        transform 260ms cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 260ms cubic-bezier(0.22, 1, 0.36, 1);
      opacity: 0;
      animation:
        teaserFadeIn 700ms 750ms cubic-bezier(0.22, 1, 0.36, 1) forwards,
        ctaPulse 2.4s 1500ms ease-in-out infinite;
    }
    .teaser-cta:hover {
      transform: translateY(-2px) scale(1.03);
      box-shadow:
        0 16px 40px -8px rgba(139, 43, 219, 0.7),
        0 0 0 8px rgba(139, 43, 219, 0.12);
    }
    .teaser-cta:active { transform: translateY(0) scale(0.98); }
    .teaser-arrow { transition: transform 260ms cubic-bezier(0.22, 1, 0.36, 1); }
    .teaser-cta:hover .teaser-arrow { transform: translateY(3px); }

    @keyframes teaserFadeIn {
      from { opacity: 0; transform: translateY(12px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes ctaPulse {
      0%, 100% { box-shadow:
          0 10px 30px -8px rgba(139, 43, 219, 0.55),
          0 0 0 0 rgba(139, 43, 219, 0.35); }
      50%      { box-shadow:
          0 14px 34px -8px rgba(139, 43, 219, 0.65),
          0 0 0 14px rgba(139, 43, 219, 0); }
    }

    /* scene ------------------------------------------------------------- */
    .intro-scene {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      transform-style: preserve-3d;
      opacity: 1;
      transition: opacity 500ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    /* Hide the phone entirely during the teaser stage — the teaser owns
       the screen and the phone shouldn't be visible or blocking clicks. */
    .intro-root[data-stage="teaser"] .intro-scene {
      opacity: 0;
      pointer-events: none;
    }

    /* Outer float layer: translateY only. During the "rising" stage it
       swoops up from below the viewport; the idle float keyframe kicks in
       once it reaches home. */
    .intro-phone-float {
      position: relative;
      width: 300px;
      height: 620px;
      transform-style: preserve-3d;
      animation: phoneFloat 6s ease-in-out infinite;
      will-change: transform;
    }
    @keyframes phoneFloat {
      0%, 100% { transform: translateY(0); }
      50%      { transform: translateY(-14px); }
    }
    /* Rising: override the idle float so the device translates in from below. */
    .intro-phone-float[data-stage="rising"] {
      animation: phoneRise 900ms cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    @keyframes phoneRise {
      0%   { transform: translateY(110vh) scale(0.9); opacity: 0; }
      60%  { opacity: 1; }
      100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    .intro-phone-float[data-stage="zooming"] { animation: none; }

    /* Inner rotation layer: straight face-on back pose → flips → zooms via transition.
       Kept square to camera (no tilt) so the device reads as a real phone on
       a shelf, not a marketing render. Depth comes from shadows + the camera
       plateau volume, not from rotating the body. */
    .intro-phone {
      position: absolute;
      inset: 0;
      transform-style: preserve-3d;
      transform: rotateX(0deg) rotateY(0deg);
      transition: transform 1500ms cubic-bezier(0.76, 0, 0.24, 1);
      will-change: transform;
    }
    .intro-phone[data-stage="flipping"],
    .intro-phone[data-stage="flipped"] {
      transform: rotateX(0deg) rotateY(180deg);
    }
    .intro-phone[data-stage="zooming"] {
      transform: rotateX(0deg) rotateY(180deg) scale(7);
      transition: transform 1200ms cubic-bezier(0.64, 0, 0.78, 0);
    }

    /* Physical depth of the device body. Used by the side-wall edges and
       the Z-separated faces. ~12px matches ~8mm iPhone thickness scaled. */
    .intro-phone { --phone-depth: 12px; }

    .phone-face {
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 48px;
      overflow: hidden;
      /* Single broad body shadow for weight — stacking multiple tight shadows
         makes the rounded-rect outline visible as "layered box lines" around
         the device. One big diffuse blur grounds it without drawing an edge.
         Inset rim lights stay, since they live *inside* the phone and sell
         the raised glass bezel without adding anything outside. */
      box-shadow:
        0 40px 90px -24px rgba(10, 9, 8, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.16),
        inset 0 -1px 0 rgba(0, 0, 0, 0.55);
    }
    .phone-face svg { width: 100%; height: 100%; display: block; }
    /* Z-separated faces so the side walls can sit in the gap between them. */
    .phone-back  { transform: translateZ(calc(var(--phone-depth) / -2)); }
    .phone-front { transform: rotateY(180deg) translateZ(calc(var(--phone-depth) / -2)); }

    .phone-chassis { position: absolute; inset: 0; }

    /* ── 3D side walls — give the phone real volume ─────────────────
       Each is a thin brushed-titanium strip rotated to face outward.
       Edge-on (invisible) when the phone is face-on in idle; they sweep into
       view during the flip at ~90° rotation, selling the device's thickness
       as it turns. Gradient picks up the body's dark titanium tone exactly —
       no inset strokes, so the seam with the front/back face has no visible
       hairline when the two meet at an angle. */
    .phone-edge {
      position: absolute;
      pointer-events: none;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      background: linear-gradient(
        180deg,
        #1c1629 0%,
        #120c1f 50%,
        #07040f 100%
      );
    }
    /* Top wall: horizontal strip, rotated to face up */
    .phone-edge-top {
      top: 0; left: 0; right: 0;
      height: var(--phone-depth);
      transform-origin: center top;
      transform: translateY(calc(var(--phone-depth) / -2)) rotateX(-90deg);
      border-radius: 48px 48px 0 0 / 12px 12px 0 0;
    }
    /* Bottom wall */
    .phone-edge-bottom {
      bottom: 0; left: 0; right: 0;
      height: var(--phone-depth);
      transform-origin: center bottom;
      transform: translateY(calc(var(--phone-depth) / 2)) rotateX(90deg);
      border-radius: 0 0 48px 48px / 0 0 12px 12px;
    }
    /* Left wall */
    .phone-edge-left {
      top: 0; bottom: 0; left: 0;
      width: var(--phone-depth);
      transform-origin: left center;
      transform: translateX(calc(var(--phone-depth) / -2)) rotateY(90deg);
      border-radius: 12px 0 0 12px / 48px 0 0 48px;
    }
    /* Right wall */
    .phone-edge-right {
      top: 0; bottom: 0; right: 0;
      width: var(--phone-depth);
      transform-origin: right center;
      transform: translateX(calc(var(--phone-depth) / 2)) rotateY(-90deg);
      border-radius: 0 12px 12px 0 / 0 48px 48px 0;
    }

    /* Screen glare — diagonal gloss stripe over the screen area only.
       Emulates a real phone glass catching ambient light. */
    .phone-glare {
      position: absolute;
      top: 14px; left: 14px; right: 14px; bottom: 14px;
      border-radius: 40px;
      pointer-events: none;
      background: linear-gradient(
        125deg,
        transparent 0%,
        transparent 42%,
        rgba(255,255,255,0.14) 48%,
        rgba(255,255,255,0.25) 50%,
        rgba(255,255,255,0.14) 52%,
        transparent 58%,
        transparent 100%
      );
      mix-blend-mode: screen;
      opacity: 0.75;
      z-index: 4;
    }

    .phone-screen {
      position: absolute;
      top: 14px; left: 14px; right: 14px; bottom: 14px;
      border-radius: 40px;
      overflow: hidden;
      background: #000;
    }

    .phone-dyn-island {
      position: absolute;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      width: 96px;
      height: 28px;
      background: #000;
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 999px;
      z-index: 3;
    }
    .island-cam {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: radial-gradient(circle at 30% 30%, #6a4f9f, #0a0612);
    }

    .screen-content {
      position: absolute;
      inset: 0;
      background: linear-gradient(160deg, #FAFAF7 0%, #F4EEFB 55%, #FAFAF7 100%);
      opacity: 0;
      transition: opacity 600ms 700ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    .intro-phone[data-stage="flipped"] .screen-content,
    .intro-phone[data-stage="zooming"] .screen-content {
      opacity: 1;
    }

    .mini-site {
      padding: 48px 20px 18px;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 9px;
      transform: scale(0.96);
      opacity: 0;
      transition:
        transform 700ms 900ms cubic-bezier(0.22, 1, 0.36, 1),
        opacity   700ms 900ms cubic-bezier(0.22, 1, 0.36, 1);
      color: #0A0908;
    }
    .intro-phone[data-stage="flipped"] .mini-site,
    .intro-phone[data-stage="zooming"] .mini-site {
      transform: scale(1);
      opacity: 1;
    }

    .mini-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 4px 2px 10px;
      border-bottom: 1px solid rgba(10,9,8,0.08);
    }
    .mini-logo {
      font-family: 'Fraunces', ui-serif, Georgia, serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.14em;
      color: #0A0908;
    }
    .mini-dots { display: inline-flex; gap: 3px; }
    .mini-dots i {
      display: inline-block;
      width: 3px; height: 3px;
      background: #78716C;
      border-radius: 50%;
    }
    .mini-eyebrow {
      font-size: 8px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #740DC2;
      margin-top: 4px;
    }
    .mini-title {
      font-family: 'Fraunces', ui-serif, Georgia, serif;
      font-size: 24px;
      line-height: 1;
      letter-spacing: -0.02em;
      margin: 0;
      font-weight: 400;
    }
    .mini-title em {
      color: #740DC2;
      font-style: italic;
    }
    .mini-sub {
      font-size: 9px;
      line-height: 1.5;
      color: #78716C;
      margin: 0;
    }
    .mini-btns { display: flex; gap: 6px; margin-top: 2px; }
    .mini-btn {
      padding: 6px 11px;
      font-size: 8.5px;
      font-weight: 500;
      border-radius: 999px;
      border: 1px solid #0A0908;
      color: #0A0908;
    }
    .mini-btn-primary {
      background: #0A0908;
      color: #FAFAF7;
    }
    .mini-card {
      margin-top: auto;
      background: #fff;
      border: 1px solid rgba(10,9,8,0.08);
      border-radius: 14px;
      padding: 9px;
      display: flex;
      gap: 10px;
      align-items: center;
      box-shadow: 0 8px 20px -10px rgba(116,13,194,0.22);
    }
    .mini-card-img {
      width: 46px; height: 46px;
      border-radius: 10px;
      background:
        radial-gradient(circle at 30% 30%, rgba(255,255,255,0.12), transparent 60%),
        linear-gradient(135deg, #1f1a2e, #3D1766);
      flex: 0 0 auto;
    }
    .mini-card-title { font-size: 10px; font-weight: 600; letter-spacing: -0.01em; }
    .mini-card-price { font-size: 9px; color: #740DC2; font-weight: 600; margin-top: 1px; }

    /* Shadow lives on the float layer so it bobs but doesn't rotate/flip.
       On the light scene, the floor shadow reads as a soft violet pool —
       grounds the device and reinforces its physicality. */
    .phone-shadow {
      position: absolute;
      left: 50%;
      bottom: -34px;
      transform: translate(-50%, 0);
      width: 72%;
      height: 32px;
      background: radial-gradient(ellipse at center, rgba(116, 13, 194, 0.28) 0%, transparent 70%);
      filter: blur(16px);
      pointer-events: none;
      z-index: -1;
    }

    .intro-root[data-stage="zooming"] .intro-bg,
    .intro-root[data-stage="zooming"] .intro-glow,
    .intro-root[data-stage="zooming"] .intro-label,
    .intro-root[data-stage="zooming"] .intro-skip,
    .intro-root[data-stage="zooming"] .phone-shadow {
      opacity: 0;
      transition: opacity 900ms 300ms cubic-bezier(0.22, 1, 0.36, 1);
    }
    .intro-root[data-stage="zooming"] .phone-face { box-shadow: none; }
    /* During zoom the phone scales 7×, which would blow the 12px depth up
       to ~84px — the side walls would read as thick bars wrapping the
       device. Fade them out before the scale kicks in so only the front
       face fills the viewport cleanly. */
    .intro-root[data-stage="zooming"] .phone-edge {
      opacity: 0;
      transition: opacity 250ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    @media (max-width: 768px) {
      .intro-phone-float { width: 220px; height: 454px; animation-duration: 8s; }
      .phone-screen { top: 10px; left: 10px; right: 10px; bottom: 10px; border-radius: 30px; }
      .phone-dyn-island { width: 72px; height: 22px; top: 9px; }
      .mini-site { padding: 38px 14px 14px; gap: 7px; }
      .mini-title { font-size: 19px; }
      .mini-sub { font-size: 8.5px; }
      .intro-skip { top: 14px; right: 14px; padding: 7px 12px; font-size: 10.5px; }
      .intro-label { top: clamp(64px, 10vh, 90px); }
      .intro-phone[data-stage="zooming"] {
        transform: rotateX(0) rotateY(180deg) scale(5.5);
      }
    }

    @media (prefers-reduced-motion: reduce) {
      .intro-root { display: none; }
    }
  `],
})
export class IntroShowcaseComponent implements OnInit, OnDestroy {
  private router = inject(Router);
  stage = signal<Stage>('done');

  private static readonly KEY = 'shahzad_intro_seen_v1';

  ngOnInit() {
    if (typeof window === 'undefined') return;

    const seen = (() => {
      try { return sessionStorage.getItem(IntroShowcaseComponent.KEY); }
      catch { return '1'; }
    })();
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const url = this.router.url.split('?')[0].split('#')[0];
    const onHome = url === '/' || url === '';

    if (seen || reduced || !onHome) return;

    // Start on the teaser — users see "Experience Shahzad Tech" + CTA first,
    // then click to bring in the phone.
    this.stage.set('teaser');
    document.body.style.overflow = 'hidden';
  }

  ngOnDestroy() {
    document.body.style.overflow = '';
  }

  @HostListener('document:keydown.escape')
  onEscape() {
    if (this.stage() !== 'done') this.finish();
  }

  onTap() {
    const s = this.stage();
    if (s === 'teaser') {
      // First click on the CTA: phone rises from below. After the rise
      // animation settles, go idle so the user can flip it.
      this.stage.set('rising');
      setTimeout(() => this.stage.set('idle'), 900);
    } else if (s === 'idle') {
      this.stage.set('flipping');
      setTimeout(() => this.stage.set('flipped'), 1500);
    } else if (s === 'flipped') {
      this.stage.set('zooming');
      setTimeout(() => this.finish(), 1250);
    }
  }

  skip(ev: Event) {
    ev.stopPropagation();
    this.finish();
  }

  private finish() {
    try { sessionStorage.setItem(IntroShowcaseComponent.KEY, '1'); } catch { /* noop */ }
    this.stage.set('done');
    document.body.style.overflow = '';
  }
}
