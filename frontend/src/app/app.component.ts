import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

import { AuthService } from './core/auth.service';
import { CartService } from './core/cart.service';
import { LanguageService } from './core/language.service';
import { ThemeService } from './core/theme.service';
import { WishlistService } from './core/wishlist.service';
import { ChatLauncherComponent } from './shared/chat-launcher.component';
import { CursorFollowerComponent } from './shared/cursor-follower.component';
import { FooterComponent } from './shared/footer.component';
import { HeaderComponent } from './shared/header.component';
import { IntroShowcaseComponent } from './shared/intro-showcase.component';
import { ScrollProgressComponent } from './shared/scroll-progress.component';
import { TawkToComponent } from './shared/tawk-to.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, RouterOutlet,
    HeaderComponent, FooterComponent, ChatLauncherComponent, TawkToComponent,
    CursorFollowerComponent, ScrollProgressComponent, IntroShowcaseComponent,
  ],
  template: `
    <app-intro-showcase />
    <app-scroll-progress />
    <app-header />
    <!-- key-bound main so <router-outlet> content fades in on every nav -->
    <main class="min-h-[calc(100vh-4rem-14rem)] page-shell" [attr.data-route]="routeKey">
      <router-outlet />
    </main>
    <app-footer />
    <app-tawk-to />
    <app-chat-launcher />
    <app-cursor-follower />
  `,
})
export class AppComponent implements OnInit {
  private auth = inject(AuthService);
  private cart = inject(CartService);
  private theme = inject(ThemeService);
  private lang = inject(LanguageService);
  // Eager-inject so its effect() starts reacting to auth state immediately.
  private wishlist = inject(WishlistService);
  private router = inject(Router);

  routeKey = 0;

  ngOnInit() {
    this.theme.init();
    this.lang.init();

    this.auth.initFromStorage()?.subscribe({
      next: () => {
        this.cart.mergeAfterLogin().subscribe();
      },
    });
    this.cart.refresh().subscribe();

    // Bump the route key on every navigation so .page-shell's children
    // re-animate via the pageIn keyframes.
    this.router.events
      .pipe(filter((e) => e instanceof NavigationEnd))
      .subscribe(() => (this.routeKey = (this.routeKey + 1) | 0));
  }
}
