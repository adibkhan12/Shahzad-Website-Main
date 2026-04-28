import { DOCUMENT } from '@angular/common';
import {
  Component, ElementRef, OnDestroy, OnInit, ViewChild, inject,
} from '@angular/core';

/**
 * Global cursor-follower: two concentric elements (dot + ring) that
 * smoothly trail the pointer via lerp in a requestAnimationFrame loop.
 *
 * - Ring enlarges and tints when hovering any <a>, <button>, [role="button"],
 *   or explicit [data-cursor="hot"] element.
 * - Shrinks briefly on pointerdown for tactile feedback.
 * - Auto-disabled on touch devices (CSS @media (pointer: coarse)).
 * - Auto-disabled if user prefers reduced motion.
 *
 * Mount once in AppComponent: <app-cursor-follower />
 */
@Component({
  selector: 'app-cursor-follower',
  standalone: true,
  template: `
    <div class="cursor-dot" #dot></div>
    <div class="cursor-ring" #ring></div>
  `,
})
export class CursorFollowerComponent implements OnInit, OnDestroy {
  @ViewChild('dot',  { static: true }) dot!: ElementRef<HTMLElement>;
  @ViewChild('ring', { static: true }) ring!: ElementRef<HTMLElement>;

  private doc = inject(DOCUMENT);
  private raf = 0;
  private target = { x: 0, y: 0 };
  private dotPos = { x: 0, y: 0 };
  private ringPos = { x: 0, y: 0 };
  private enabled = true;

  private onMove = (e: PointerEvent) => {
    this.target.x = e.clientX;
    this.target.y = e.clientY;
  };
  private onEnter = (e: Event) => {
    const t = e.target as HTMLElement | null;
    if (!t) return;
    if (t.matches('a, button, [role="button"], [data-cursor="hot"]')) {
      this.ring.nativeElement.classList.add('hot');
    }
  };
  private onLeave = (e: Event) => {
    const t = e.target as HTMLElement | null;
    if (!t) return;
    if (t.matches('a, button, [role="button"], [data-cursor="hot"]')) {
      this.ring.nativeElement.classList.remove('hot');
    }
  };
  private onDown = () => this.ring.nativeElement.classList.add('click');
  private onUp   = () => this.ring.nativeElement.classList.remove('click');

  ngOnInit() {
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const touch = matchMedia('(pointer: coarse)').matches;
    if (reduced || touch) { this.enabled = false; return; }

    this.doc.documentElement.classList.add('has-cursor-follower');
    window.addEventListener('pointermove', this.onMove, { passive: true });
    document.addEventListener('pointerover', this.onEnter, true);
    document.addEventListener('pointerout', this.onLeave, true);
    window.addEventListener('pointerdown', this.onDown);
    window.addEventListener('pointerup', this.onUp);

    const loop = () => {
      // Lerp both elements toward target; dot is snappier, ring lags.
      this.dotPos.x += (this.target.x - this.dotPos.x) * 0.4;
      this.dotPos.y += (this.target.y - this.dotPos.y) * 0.4;
      this.ringPos.x += (this.target.x - this.ringPos.x) * 0.18;
      this.ringPos.y += (this.target.y - this.ringPos.y) * 0.18;
      const d = this.dot.nativeElement;
      const r = this.ring.nativeElement;
      d.style.transform = `translate3d(${this.dotPos.x}px, ${this.dotPos.y}px, 0) translate(-50%, -50%)`;
      r.style.transform = `translate3d(${this.ringPos.x}px, ${this.ringPos.y}px, 0) translate(-50%, -50%)`;
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  ngOnDestroy() {
    if (!this.enabled) return;
    cancelAnimationFrame(this.raf);
    this.doc.documentElement.classList.remove('has-cursor-follower');
    window.removeEventListener('pointermove', this.onMove);
    document.removeEventListener('pointerover', this.onEnter, true);
    document.removeEventListener('pointerout', this.onLeave, true);
    window.removeEventListener('pointerdown', this.onDown);
    window.removeEventListener('pointerup', this.onUp);
  }
}
