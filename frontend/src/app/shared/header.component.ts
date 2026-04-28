import { CommonModule } from '@angular/common';
import { Component, HostListener, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NavigationEnd, Router, RouterLink, RouterLinkActive } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { filter } from 'rxjs';

import { AuthService } from '../core/auth.service';
import { CartService } from '../core/cart.service';
import { LanguageService } from '../core/language.service';
import { ThemeService } from '../core/theme.service';
import { WishlistService } from '../core/wishlist.service';
import { LogoComponent } from './logo.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RouterLinkActive, LogoComponent, TranslateModule],
  template: `
    <header class="nav-glass" [class.is-scrolled]="scrolled()">
      <div class="container-x h-16 flex items-center gap-3 md:gap-6">
        <button type="button"
                class="lg:hidden w-9 h-9 inline-flex items-center justify-center rounded-full hover:bg-neutral-100 dark:hover:bg-white/10 transition"
                (click)="mobileOpen.set(!mobileOpen())"
                [attr.aria-label]="mobileOpen() ? ('common.close' | translate) : ('nav.shop' | translate)"
                [attr.aria-expanded]="mobileOpen()">
          <svg *ngIf="!mobileOpen()" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">
            <path d="M3 6h18M3 12h18M3 18h18"/>
          </svg>
          <svg *ngIf="mobileOpen()" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18"/>
          </svg>
        </button>

        <a routerLink="/" class="flex items-center group shrink-0" [attr.aria-label]="'brand' | translate">
          <app-logo class="hidden sm:inline-flex" variant="lockup" [size]="36"></app-logo>
          <app-logo class="sm:hidden" variant="badge" [size]="32"></app-logo>
        </a>

        <nav class="hidden lg:flex items-center gap-1 ms-4">
          <a routerLink="/products" routerLinkActive="!text-ink dark:!text-white" [routerLinkActiveOptions]="{exact: false}"
             class="px-3 py-1.5 text-sm rounded-full transition">{{ 'nav.shop' | translate }}</a>
          <a routerLink="/repairs" routerLinkActive="!text-ink dark:!text-white"
             class="px-3 py-1.5 text-sm rounded-full transition">{{ 'nav.repairs' | translate }}</a>
          <a routerLink="/orders/track" routerLinkActive="!text-ink dark:!text-white"
             class="px-3 py-1.5 text-sm rounded-full transition">{{ 'nav.trackOrder' | translate }}</a>
          <a routerLink="/about" routerLinkActive="!text-ink dark:!text-white"
             class="px-3 py-1.5 text-sm rounded-full transition">{{ 'nav.about' | translate }}</a>
        </nav>

        <form class="flex-1 min-w-0 max-w-md ms-auto relative" (ngSubmit)="search()">
          <svg class="absolute start-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <circle cx="11" cy="11" r="7"/><path d="m21 21-3.5-3.5"/>
          </svg>
          <input [(ngModel)]="query" name="q" [placeholder]="'nav.searchPlaceholder' | translate"
                 class="w-full h-9 ps-10 pe-3 text-sm rounded-full border border-neutral-200 bg-neutral-50/60 focus:border-ink focus:bg-white focus:outline-none transition" />
        </form>

        <a *ngIf="auth.isAuthenticated()" routerLink="/wishlist"
           class="relative hidden md:inline-flex w-9 h-9 items-center justify-center rounded-full hover:bg-neutral-100 dark:hover:bg-white/10 transition"
           [attr.aria-label]="'nav.wishlist' | translate">
          <svg class="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor"
               stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
          <span *ngIf="wishlist.count() > 0"
                class="absolute -top-0.5 -end-0.5 min-w-[18px] h-[18px] px-1 rounded-full bg-pink-500 text-white text-[10px] font-semibold flex items-center justify-center">
            {{ wishlist.count() > 99 ? '99+' : wishlist.count() }}
          </span>
        </a>
        <a routerLink="/cart" class="relative w-9 h-9 inline-flex items-center justify-center rounded-full hover:bg-neutral-100 dark:hover:bg-white/10 transition" [attr.aria-label]="'nav.cart' | translate">
          <svg class="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75">
            <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13 5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17"/>
            <circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/>
          </svg>
          <span *ngIf="cart.count() > 0"
                class="absolute -top-0.5 -end-0.5 min-w-[18px] h-[18px] px-1 bg-ink text-white text-[10px] font-medium rounded-full flex items-center justify-center animate-fade-in">
            {{ cart.count() }}
          </span>
        </a>

        <!-- Language toggle: EN ⇄ AR, flips <html dir> + reloads translations -->
        <button type="button"
                (click)="lang.toggle()"
                class="hidden sm:inline-flex h-9 items-center justify-center rounded-full px-3 text-[11px] font-semibold tracking-wider hover:bg-neutral-100 dark:hover:bg-white/10 transition"
                [attr.aria-label]="lang.current() === 'ar' ? 'Switch to English' : 'التبديل إلى العربية'">
          {{ lang.current() === 'ar' ? 'EN' : 'AR' }}
        </button>

        <button type="button"
                (click)="theme.toggle()"
                class="hidden sm:inline-flex w-9 h-9 items-center justify-center rounded-full hover:bg-neutral-100 dark:hover:bg-white/10 transition"
                [attr.aria-label]="theme.mode() === 'dark' ? ('nav.lightMode' | translate) : ('nav.darkMode' | translate)">
          <svg *ngIf="theme.mode() === 'dark'" class="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">
            <circle cx="12" cy="12" r="4"/>
            <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
          </svg>
          <svg *ngIf="theme.mode() === 'light'" class="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75" aria-hidden="true">
            <path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79Z"/>
          </svg>
        </button>
        <div class="w-px h-6 bg-neutral-200 dark:bg-white/15 hidden md:block"></div>
        <ng-container *ngIf="auth.user() as u; else loginLink">
          <div class="relative" (click)="$event.stopPropagation()">
            <button class="inline-flex items-center gap-2 text-sm text-neutral-700 hover:text-ink transition" (click)="menuOpen.set(!menuOpen())">
              <span class="w-7 h-7 rounded-full bg-neutral-900 text-white flex items-center justify-center text-[11px] font-medium">
                {{ (u.full_name || u.email).charAt(0).toUpperCase() }}
              </span>
              <span class="hidden md:inline">{{ firstName(u) }}</span>
            </button>
            <div *ngIf="menuOpen()"
                 class="absolute end-0 mt-2 w-52 rounded-2xl bg-white border border-neutral-200 shadow-lift py-1.5 animate-slide-up">
              <div class="px-3 py-2 border-b border-neutral-100">
                <div class="text-xs text-neutral-500">{{ 'nav.signedInAs' | translate }}</div>
                <div class="text-sm font-medium truncate">{{ u.email }}</div>
              </div>
              <a routerLink="/account" (click)="menuOpen.set(false)" class="block px-3 py-2 text-sm hover:bg-neutral-50">{{ 'nav.dashboard' | translate }}</a>
              <a routerLink="/orders" (click)="menuOpen.set(false)" class="block px-3 py-2 text-sm hover:bg-neutral-50">{{ 'nav.myOrders' | translate }}</a>
              <a routerLink="/account/addresses" (click)="menuOpen.set(false)" class="block px-3 py-2 text-sm hover:bg-neutral-50">{{ 'nav.addresses' | translate }}</a>
              <button (click)="menuOpen.set(false); auth.logout()" class="w-full text-start px-3 py-2 text-sm hover:bg-neutral-50 text-red-600">{{ 'nav.signOut' | translate }}</button>
            </div>
          </div>
        </ng-container>
        <ng-template #loginLink>
          <a routerLink="/account/login" class="hidden sm:inline-flex btn-outline !px-4 !py-1.5 !text-sm">{{ 'nav.signIn' | translate }}</a>
        </ng-template>
      </div>

      <!-- Mobile menu drawer -->
      <div *ngIf="mobileOpen()"
           class="lg:hidden border-t border-neutral-200/70 dark:border-white/10
                  bg-white/95 dark:bg-[#0A0B1A]/95 backdrop-blur-lg animate-slide-up">
        <nav class="container-x py-3 flex flex-col gap-0.5 text-[15px]">
          <a routerLink="/products"    (click)="mobileOpen.set(false)" class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition">{{ 'nav.shop' | translate }}</a>
          <a routerLink="/repairs"     (click)="mobileOpen.set(false)" class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition">{{ 'nav.repairs' | translate }}</a>
          <a routerLink="/orders/track"(click)="mobileOpen.set(false)" class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition">{{ 'nav.trackOrder' | translate }}</a>
          <a routerLink="/about"       (click)="mobileOpen.set(false)" class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition">{{ 'nav.about' | translate }}</a>
          <div class="hairline my-2"></div>
          <a *ngIf="auth.isAuthenticated()" routerLink="/wishlist" (click)="mobileOpen.set(false)"
             class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition flex items-center justify-between">
            <span>{{ 'nav.wishlist' | translate }}</span>
            <span *ngIf="wishlist.count() > 0"
                  class="min-w-[20px] h-[20px] px-1.5 rounded-full bg-pink-500 text-white text-[11px] font-semibold flex items-center justify-center">
              {{ wishlist.count() }}
            </span>
          </a>
          <a *ngIf="!auth.isAuthenticated()" routerLink="/account/login" (click)="mobileOpen.set(false)" class="py-3 px-2 rounded-md hover:bg-neutral-100 dark:hover:bg-white/5 transition">{{ 'nav.signIn' | translate }}</a>
          <button (click)="lang.toggle()" class="py-3 px-2 rounded-md text-start hover:bg-neutral-100 dark:hover:bg-white/5 transition">
            {{ lang.current() === 'ar' ? 'English' : 'العربية' }}
          </button>
          <button (click)="theme.toggle()" class="py-3 px-2 rounded-md text-start hover:bg-neutral-100 dark:hover:bg-white/5 transition">
            {{ theme.mode() === 'dark' ? ('nav.lightMode' | translate) : ('nav.darkMode' | translate) }}
          </button>
        </nav>
      </div>
    </header>
  `,
})
export class HeaderComponent implements OnInit {
  auth = inject(AuthService);
  cart = inject(CartService);
  theme = inject(ThemeService);
  wishlist = inject(WishlistService);
  lang = inject(LanguageService);
  private router = inject(Router);
  menuOpen = signal(false);
  mobileOpen = signal(false);
  scrolled = signal(false);
  query = '';

  ngOnInit() {
    this.router.events
      .pipe(filter((e) => e instanceof NavigationEnd))
      .subscribe(() => {
        this.mobileOpen.set(false);
        this.menuOpen.set(false);
      });
  }

  @HostListener('window:scroll')
  onScroll() {
    this.scrolled.set(window.scrollY > 4);
  }

  @HostListener('document:click')
  onDocumentClick() {
    if (this.menuOpen()) this.menuOpen.set(false);
  }

  @HostListener('document:keydown.escape')
  onEscape() {
    this.menuOpen.set(false);
    this.mobileOpen.set(false);
  }

  firstName(u: any): string {
    return (u.first_name || (u.full_name || u.email).split(' ')[0] || '').slice(0, 14);
  }

  search() {
    this.router.navigate(['/products'], { queryParams: { q: this.query || null } });
  }
}
