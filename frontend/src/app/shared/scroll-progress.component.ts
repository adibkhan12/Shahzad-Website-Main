import {
  Component, ElementRef, HostBinding, OnDestroy, OnInit, ViewChild,
} from '@angular/core';

/**
 * Fixed 2-px progress bar at the top of the viewport that fills as the
 * user scrolls through the page. rAF-throttled, transform-driven (GPU).
 *
 * Uses the global --progress custom property on the host's ::after pseudo
 * (defined in styles.scss under .scroll-progress).
 */
@Component({
  selector: 'app-scroll-progress',
  standalone: true,
  template: `<div #bar class="scroll-progress"></div>`,
})
export class ScrollProgressComponent implements OnInit, OnDestroy {
  @ViewChild('bar', { static: true }) bar!: ElementRef<HTMLElement>;

  private raf = 0;
  private pending = false;

  private update = () => {
    const doc = document.documentElement;
    const max = (doc.scrollHeight - doc.clientHeight) || 1;
    const p = Math.max(0, Math.min(1, window.scrollY / max));
    this.bar.nativeElement.style.setProperty('--progress', String(p));
    this.pending = false;
  };

  private onScroll = () => {
    if (this.pending) return;
    this.pending = true;
    this.raf = requestAnimationFrame(this.update);
  };

  ngOnInit() {
    window.addEventListener('scroll', this.onScroll, { passive: true });
    window.addEventListener('resize', this.onScroll, { passive: true });
    this.update();
  }

  ngOnDestroy() {
    cancelAnimationFrame(this.raf);
    window.removeEventListener('scroll', this.onScroll);
    window.removeEventListener('resize', this.onScroll);
  }
}
