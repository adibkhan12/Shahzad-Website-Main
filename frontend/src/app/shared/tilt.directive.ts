import {
  Directive, ElementRef, HostListener, Input, OnInit, inject,
} from '@angular/core';

/**
 * 3D tilt on hover — the card rotates toward the pointer, producing a
 * subtle parallax depth effect. Pairs with the `.tilt-stage` parent class
 * (which sets the CSS `perspective`).
 *
 * Usage:
 *   <div class="tilt-stage">
 *     <div appTilt [max]="6" class="tilt-inner card">
 *       ...
 *       <img data-depth style="--depth: 20px" />  <!-- pops forward -->
 *     </div>
 *   </div>
 *
 * - `max` is the maximum rotation in degrees (default 6°; more is garish).
 * - rAF-throttled; only manipulates transform + CSS vars.
 * - Disabled on touch / reduced-motion.
 */
@Directive({
  selector: '[appTilt]',
  standalone: true,
  host: { 'class': 'tilt-inner' },
})
export class TiltDirective implements OnInit {
  @Input() max = 6;

  private host = inject(ElementRef<HTMLElement>);
  private raf = 0;
  private enabled = true;

  ngOnInit() {
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const touch   = matchMedia('(pointer: coarse)').matches;
    this.enabled = !(reduced || touch);
  }

  @HostListener('pointermove', ['$event'])
  onMove(e: PointerEvent) {
    if (!this.enabled) return;
    const el = this.host.nativeElement;
    const r = el.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width;  // 0..1
    const py = (e.clientY - r.top)  / r.height; // 0..1
    const rx = (0.5 - py) * this.max;  // rotate around X axis
    const ry = (px - 0.5) * this.max;  // rotate around Y axis
    // Also set --mx/--my so any child using cursor-glow gets spec-compliant coords
    el.style.setProperty('--mx', `${px * 100}%`);
    el.style.setProperty('--my', `${py * 100}%`);
    this.schedule(rx, ry);
  }

  @HostListener('pointerleave')
  onLeave() {
    if (!this.enabled) return;
    this.schedule(0, 0);
  }

  private schedule(rx: number, ry: number) {
    cancelAnimationFrame(this.raf);
    this.raf = requestAnimationFrame(() => {
      this.host.nativeElement.style.transform =
        `rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg)`;
    });
  }
}
