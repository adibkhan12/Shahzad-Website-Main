import { Directive, ElementRef, Input, OnDestroy, OnInit, inject } from '@angular/core';

/**
 * Fades + lifts an element on its first scroll into view.
 * Usage:  <div appReveal>…</div>
 *         <div appReveal="200">…</div>  // 200ms stagger delay
 */
@Directive({
  selector: '[appReveal]',
  standalone: true,
})
export class RevealDirective implements OnInit, OnDestroy {
  @Input('appReveal') delay: number | string = 0;

  private el = inject(ElementRef<HTMLElement>);
  private observer?: IntersectionObserver;

  ngOnInit() {
    const node = this.el.nativeElement;
    node.style.opacity = '0';
    node.style.transform = 'translateY(22px)';
    node.style.filter = 'blur(2px)';
    // Slower, cinematic easing — still feels responsive on fast scroll
    node.style.transition =
      'opacity 1200ms cubic-bezier(0.22,1,0.36,1), ' +
      'transform 1200ms cubic-bezier(0.22,1,0.36,1), ' +
      'filter 900ms cubic-bezier(0.22,1,0.36,1)';
    node.style.willChange = 'opacity, transform, filter';
    node.style.transitionDelay = `${+this.delay}ms`;

    if (typeof IntersectionObserver === 'undefined') {
      this.reveal(node);
      return;
    }
    this.observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            this.reveal(e.target as HTMLElement);
            this.observer?.unobserve(e.target);
          }
        }
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' },
    );
    this.observer.observe(node);
  }

  private reveal(node: HTMLElement) {
    node.style.opacity = '1';
    node.style.transform = 'translateY(0)';
    node.style.filter = 'blur(0)';
  }

  ngOnDestroy() {
    this.observer?.disconnect();
  }
}
