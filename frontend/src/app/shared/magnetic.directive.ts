import {
  Directive, ElementRef, HostListener, Input, OnInit, inject,
} from '@angular/core';

/**
 * Magnetic attraction: the element is pulled a fraction of the distance
 * between its centre and the cursor, creating the subtle "drag toward me"
 * feel used by premium tech sites.
 *
 * Usage:   <a appMagnetic class="btn btn-primary">Shop</a>
 *          <button appMagnetic [strength]="0.35">CTA</button>
 *
 * - Strength 0…1 (default 0.25). 0.15–0.3 is the sweet spot for buttons.
 * - Auto-disabled on touch devices and reduced-motion users.
 * - rAF-throttled; transforms are GPU-composited.
 */
@Directive({
  selector: '[appMagnetic]',
  standalone: true,
  host: { 'class': 'magnetic' },
})
export class MagneticDirective implements OnInit {
  @Input() strength = 0.25;

  private host = inject(ElementRef<HTMLElement>);
  private raf = 0;
  private tx = 0; private ty = 0;
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
    const dx = e.clientX - r.left - r.width / 2;
    const dy = e.clientY - r.top  - r.height / 2;
    this.tx = dx * this.strength;
    this.ty = dy * this.strength;
    this.schedule();
  }

  @HostListener('pointerleave')
  onLeave() {
    if (!this.enabled) return;
    this.tx = 0; this.ty = 0;
    this.schedule();
  }

  private schedule() {
    cancelAnimationFrame(this.raf);
    this.raf = requestAnimationFrame(() => {
      this.host.nativeElement.style.transform =
        `translate3d(${this.tx.toFixed(2)}px, ${this.ty.toFixed(2)}px, 0)`;
    });
  }
}
