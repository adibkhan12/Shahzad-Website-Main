import { CommonModule } from '@angular/common';
import { Component, OnInit, effect, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { forkJoin } from 'rxjs';

import { environment } from '../../../environments/environment';
import { ApiService } from '../../core/api.service';
import { LanguageService } from '../../core/language.service';
import { Banner, Category, Paginated, Product } from '../../core/models';
import { MagneticDirective } from '../../shared/magnetic.directive';
import { ProductCardComponent } from '../../shared/product-card.component';
import { RevealDirective } from '../../shared/reveal.directive';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, ProductCardComponent, RevealDirective, MagneticDirective, TranslateModule],
  template: `
    <!-- HERO -->
    <section class="relative overflow-hidden grid-mesh bg-gradient-to-br from-neutral-50 via-white to-brand-50/40 dark:from-neutral-950 dark:via-black dark:to-[#1a0430]">
      <div class="container-x pt-16 md:pt-24 pb-16 md:pb-28 grid md:grid-cols-12 gap-10 items-center">
        <div class="md:col-span-6" appReveal>
          <div class="eyebrow">{{ 'home.eyebrow' | translate }}</div>
          <h1 class="display text-5xl md:text-7xl tracking-tight leading-[0.95] mt-5">
            {{ 'home.heroTitle1' | translate }}<br/>
            <em class="text-brand">{{ 'home.heroTitle2' | translate }}</em>
          </h1>
          <p class="mt-6 text-neutral-600 max-w-md text-[15px] leading-relaxed"
             [innerHTML]="'home.heroDesc' | translate"></p>
          <div class="mt-8 flex items-center gap-3">
            <a routerLink="/products" appMagnetic [strength]="0.25" class="btn btn-primary btn-futura">
              {{ 'home.browseInventory' | translate }}
              <svg class="w-4 h-4 dir-flip" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M13 6l6 6-6 6"/>
              </svg>
            </a>
            <a routerLink="/repairs" appMagnetic [strength]="0.18" class="btn btn-outline">{{ 'home.onsiteRepairs' | translate }}</a>
          </div>
          <div class="mt-12 flex items-center gap-8 text-xs text-neutral-500">
            <div>
              <div class="text-ink text-lg font-semibold">{{ 'home.yearsBadge' | translate }}</div>
              <div>{{ 'home.yearsLabel' | translate }}</div>
            </div>
            <div class="w-px h-10 bg-neutral-200"></div>
            <div>
              <div class="text-ink text-lg font-semibold">{{ 'home.sameDayBadge' | translate }}</div>
              <div>{{ 'home.sameDayLabel' | translate }}</div>
            </div>
            <div class="w-px h-10 bg-neutral-200"></div>
            <div>
              <div class="text-ink text-lg font-semibold">{{ 'home.weBuyBadge' | translate }}</div>
              <div>{{ 'home.weBuyLabel' | translate }}</div>
            </div>
          </div>
        </div>
        <div class="md:col-span-6" appReveal="120">
          <div class="hero-reveal relative aspect-[4/5] rounded-3xl overflow-hidden bg-neutral-950"
               (mousemove)="onHeroMove($event)"
               (mouseleave)="onHeroLeave($event)"
               (touchstart)="onHeroTouchStart($event)"
               (touchmove)="onHeroTouchMove($event)"
               (touchend)="onHeroTouchEnd($event)"
               (touchcancel)="onHeroTouchEnd($event)">
            <ng-container *ngIf="featured()[0] as hero">
              <img *ngIf="hero.primary_image" [src]="hero.primary_image" [alt]="hero.title"
                   loading="eager" decoding="async" fetchpriority="high"
                   class="hero-base absolute inset-0 w-full h-full object-cover" />
              <img *ngIf="hero.primary_image" [src]="hero.primary_image" alt="" aria-hidden="true"
                   loading="eager" decoding="async"
                   class="hero-desat absolute inset-0 w-full h-full object-cover pointer-events-none" />
              <div class="absolute inset-x-0 bottom-0 p-6 md:p-8 bg-gradient-to-t from-black/70 to-transparent">
                <div class="eyebrow text-neutral-300">{{ 'home.featuredEyebrow' | translate }}</div>
                <div class="mt-1">
                  <div class="text-white text-2xl font-semibold tracking-tight">{{ hero.title }}</div>
                  <div class="mt-1 text-neutral-300 text-sm">
                    <ng-container *ngIf="hero.on_sale; else heroPrice">
                      <span class="text-white">{{ hero.sale_price }} {{ 'common.currency' | translate }}</span>
                      <span class="ms-2 line-through opacity-60">{{ hero.price }}</span>
                    </ng-container>
                    <ng-template #heroPrice>{{ 'product.from' | translate }} {{ hero.price }} {{ 'common.currency' | translate }}</ng-template>
                  </div>
                  <a [routerLink]="['/products', hero.slug]" class="mt-4 inline-flex items-center gap-2 text-sm text-white">
                    {{ 'home.explore' | translate }}
                    <svg class="w-3.5 h-3.5 dir-flip" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
                  </a>
                </div>
              </div>
            </ng-container>
          </div>
        </div>
      </div>
    </section>

    <!-- VALUE STRIP -->
    <section class="container-x py-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-5 rounded-2xl border border-neutral-200/70" appReveal="0">
          <div class="text-xl">🤝</div>
          <div class="mt-2 font-medium text-sm">{{ 'home.weResell' | translate }}</div>
          <div class="text-xs text-neutral-500 mt-0.5">{{ 'home.weResellDesc' | translate }}</div>
        </div>
        <div class="p-5 rounded-2xl border border-neutral-200/70" appReveal="80">
          <div class="text-xl">💵</div>
          <div class="mt-2 font-medium text-sm">{{ 'home.weBuy' | translate }}</div>
          <div class="text-xs text-neutral-500 mt-0.5">{{ 'home.weBuyDesc' | translate }}</div>
        </div>
        <div class="p-5 rounded-2xl border border-neutral-200/70" appReveal="160">
          <div class="text-xl">🔧</div>
          <div class="mt-2 font-medium text-sm">{{ 'home.weRepair' | translate }}</div>
          <div class="text-xs text-neutral-500 mt-0.5">{{ 'home.weRepairDesc' | translate }}</div>
        </div>
        <div class="p-5 rounded-2xl border border-neutral-200/70" appReveal="240">
          <div class="text-xl">🛡️</div>
          <div class="mt-2 font-medium text-sm">{{ 'home.warranty' | translate }}</div>
          <div class="text-xs text-neutral-500 mt-0.5">{{ 'home.warrantyDesc' | translate }}</div>
        </div>
      </div>
    </section>

    <!-- BANNERS -->
    <section *ngIf="banners().length" class="container-x py-12">
      <div class="grid md:grid-cols-3 gap-4">
        <a *ngFor="let b of banners(); let i = index" [href]="b.link || '#'"
           [appReveal]="i * 100"
           class="group relative overflow-hidden rounded-2xl p-8 min-h-[200px] flex flex-col justify-between text-white transition-transform duration-500 ease-smooth hover:-translate-y-0.5"
           [style.background]="b.bg">
          <div>
            <h3 class="display text-2xl md:text-3xl leading-tight">{{ b.title }}</h3>
            <p class="text-sm opacity-85 mt-2 max-w-xs">{{ b.desc }}</p>
          </div>
          <span *ngIf="b.button" class="inline-flex items-center gap-2 text-sm font-medium">
            {{ b.button }}
            <svg class="w-3.5 h-3.5 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </span>
        </a>
      </div>
    </section>

    <!-- CATEGORIES -->
    <section class="container-x py-12">
      <div class="flex items-end justify-between mb-8" appReveal>
        <div>
          <div class="eyebrow">{{ 'home.categoriesEyebrow' | translate }}</div>
          <h2 class="display text-3xl md:text-4xl mt-1">{{ 'home.categoriesTitle' | translate }}</h2>
        </div>
        <a routerLink="/products" class="hidden md:inline text-sm text-neutral-500 hover:text-ink transition">{{ 'home.viewAll' | translate }} →</a>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        <a *ngFor="let c of categories(); let i = index" [routerLink]="['/categories', c.slug]"
           [appReveal]="i * 40"
           class="group p-5 rounded-2xl border border-neutral-200/70 hover:border-ink hover:bg-neutral-50 transition-all duration-300 ease-smooth">
          <div class="text-sm font-medium group-hover:translate-x-0.5 transition">{{ c.name }}</div>
          <div class="text-xs text-neutral-500 mt-1">{{ 'home.exploreArrow' | translate }}</div>
        </a>
      </div>
    </section>

    <!-- BESTSELLERS -->
    <section class="container-x py-12">
      <div class="flex items-end justify-between mb-8" appReveal>
        <div>
          <div class="eyebrow">{{ 'home.bestsellersEyebrow' | translate }}</div>
          <h2 class="display text-3xl md:text-4xl mt-1">{{ 'home.bestsellersTitle' | translate }}</h2>
          <p class="text-sm text-neutral-500 mt-1">{{ 'home.bestsellersDesc' | translate }}</p>
        </div>
        <a routerLink="/products" class="hidden md:inline text-sm text-neutral-500 hover:text-ink transition">{{ 'home.seeAll' | translate }} →</a>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
        <div *ngFor="let p of bestsellers(); let i = index" [appReveal]="i * 50">
          <app-product-card [product]="p" />
        </div>
      </div>
    </section>

    <!-- FEATURED -->
    <section *ngIf="featured().length" class="container-x py-12">
      <div class="flex items-end justify-between mb-8" appReveal>
        <div>
          <div class="eyebrow">{{ 'home.featuredHeadingEyebrow' | translate }}</div>
          <h2 class="display text-3xl md:text-4xl mt-1">{{ 'home.featuredHeading' | translate }}</h2>
        </div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
        <div *ngFor="let p of featured(); let i = index" [appReveal]="i * 50">
          <app-product-card [product]="p" />
        </div>
      </div>
    </section>

    <!-- BRAND SECTIONS -->
    <section *ngFor="let brand of brandSections()" class="container-x py-12">
      <div class="flex items-end justify-between mb-8" appReveal>
        <div>
          <div class="eyebrow">{{ 'home.brandSpotlightEyebrow' | translate }}</div>
          <h2 class="display text-3xl md:text-4xl mt-1">{{ brand.name }}</h2>
          <p class="text-sm text-neutral-500 mt-1">{{ (brand.name === 'Apple' ? 'home.appleTagline' : 'home.samsungTagline') | translate }}</p>
        </div>
        <a [routerLink]="['/products']" [queryParams]="{q: brand.name}" class="hidden md:inline text-sm text-neutral-500 hover:text-ink transition">
          {{ 'home.allBrand' | translate: { brand: brand.name } }}
        </a>
      </div>
      <div *ngIf="brand.products.length; else noBrandProducts"
           class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
        <div *ngFor="let p of brand.products; let i = index" [appReveal]="i * 50">
          <app-product-card [product]="p" />
        </div>
      </div>
      <ng-template #noBrandProducts>
        <p class="text-sm text-neutral-500">{{ 'home.noBrandStock' | translate: { brand: brand.name } }}</p>
      </ng-template>
    </section>

    <!-- NEW ARRIVALS -->
    <section class="container-x py-12 pb-20">
      <div class="flex items-end justify-between mb-8" appReveal>
        <div>
          <div class="eyebrow">{{ 'home.newArrivalsEyebrow' | translate }}</div>
          <h2 class="display text-3xl md:text-4xl mt-1">{{ 'home.newArrivalsTitle' | translate }}</h2>
        </div>
        <a routerLink="/products" class="hidden md:inline text-sm text-neutral-500 hover:text-ink transition">{{ 'home.seeAll' | translate }} →</a>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
        <div *ngFor="let p of latest(); let i = index" [appReveal]="i * 50">
          <app-product-card [product]="p" />
        </div>
      </div>
    </section>

    <!-- SELL YOUR DEVICE -->
    <section class="container-x pb-12">
      <div appReveal class="on-dark rounded-3xl p-10 md:p-16 grid md:grid-cols-2 gap-8 items-center overflow-hidden relative">
        <div class="absolute -top-10 -right-10 w-56 h-56 rounded-full bg-white/10 blur-3xl"></div>
        <div class="absolute -bottom-10 -left-10 w-56 h-56 rounded-full bg-black/10 blur-3xl"></div>
        <div class="relative">
          <div class="eyebrow text-brand-100">{{ 'home.tradeInEyebrow' | translate }}</div>
          <h3 class="display text-3xl md:text-5xl tracking-tight leading-tight mt-2">
            {{ 'home.tradeInTitle' | translate }}<br/><em class="text-white/90">{{ 'home.tradeInSubtitle' | translate }}</em>
          </h3>
          <p class="mt-4 text-brand-100 text-sm max-w-md">{{ 'home.tradeInDesc' | translate }}</p>
        </div>
        <div class="relative flex md:justify-end">
          <a [href]="'https://wa.me/' + whatsapp" target="_blank"
             class="btn bg-white text-ink hover:bg-neutral-200">
            <svg class="w-4 h-4 text-[#25D366]" fill="currentColor" viewBox="0 0 24 24"><path d="M20.52 3.48A11.78 11.78 0 0 0 12.06 0C5.5 0 .17 5.32.17 11.88a11.81 11.81 0 0 0 1.62 5.95L0 24l6.34-1.66a11.8 11.8 0 0 0 5.72 1.46h.01c6.56 0 11.89-5.32 11.89-11.88a11.79 11.79 0 0 0-3.45-8.44"/></svg>
            {{ 'home.tradeInCta' | translate }}
          </a>
        </div>
      </div>
    </section>

    <!-- ON-SITE REPAIRS -->
    <section class="container-x pb-20">
      <div appReveal class="on-dark rounded-3xl p-10 md:p-16 grid md:grid-cols-2 gap-8 items-center">
        <div>
          <div class="eyebrow text-neutral-400">{{ 'home.repairsCtaEyebrow' | translate }}</div>
          <h3 class="display text-3xl md:text-5xl tracking-tight leading-tight mt-2">
            {{ 'home.repairsCtaTitle1' | translate }}<br/><em class="text-brand-300">{{ 'home.repairsCtaTitle2' | translate }}</em>
          </h3>
          <p class="mt-4 text-neutral-400 text-sm max-w-md">{{ 'home.repairsCtaDesc' | translate }}</p>
        </div>
        <div class="flex md:justify-end">
          <a routerLink="/repairs" class="btn bg-white text-ink hover:bg-neutral-200">{{ 'home.bookRepair' | translate }}</a>
        </div>
      </div>
    </section>
  `,
})
export class HomeComponent implements OnInit {
  private api = inject(ApiService);
  private lang = inject(LanguageService);
  banners = signal<Banner[]>([]);
  categories = signal<Category[]>([]);
  featured = signal<Product[]>([]);
  bestsellers = signal<Product[]>([]);
  latest = signal<Product[]>([]);

  constructor() {
    // Re-fetch banners whenever the language changes. Banner title/desc/button
    // are localized server-side via Accept-Language, so a lang flip means the
    // cached English copy is stale. Other lists (products/categories) aren't
    // localized yet — no need to refetch them until their models grow _ar fields.
    effect(() => {
      // Touch the signal so the effect re-runs when the active lang changes.
      this.lang.current();
      this.api
        .get<{ banners: Banner[]; settings: any }>('/core/config/')
        .subscribe((c) => this.banners.set(c.banners || []));
    });
  }

  brandSections = signal<{ name: string; tagline: string; products: Product[] }[]>([
    { name: 'Apple', tagline: 'iPhone, MacBook, iPad, Watch — hand-tested.', products: [] },
    { name: 'Samsung', tagline: 'Galaxy phones, tablets, and storage.', products: [] },
  ]);

  whatsapp = environment.whatsappNumber;

  /** Tracks the cursor inside the hero image. The CSS reveal mask uses --mx/--my
   *  to place a soft hole in the grayscale overlay, exposing the original colors. */
  onHeroMove(ev: MouseEvent) {
    const el = ev.currentTarget as HTMLElement;
    const rect = el.getBoundingClientRect();
    const mx = ((ev.clientX - rect.left) / rect.width) * 100;
    const my = ((ev.clientY - rect.top) / rect.height) * 100;
    el.style.setProperty('--mx', `${mx}%`);
    el.style.setProperty('--my', `${my}%`);
  }

  /** Push the reveal hole off-canvas so the hero returns to fully desaturated. */
  onHeroLeave(ev: MouseEvent) {
    const el = ev.currentTarget as HTMLElement;
    el.style.setProperty('--mx', '-999px');
    el.style.setProperty('--my', '-999px');
  }

  // ── Touch: finger-driven reveal (overrides the CSS auto-orbit on mobile) ──
  private touchReleaseTimer?: ReturnType<typeof setTimeout>;

  onHeroTouchStart(ev: TouchEvent) {
    const el = ev.currentTarget as HTMLElement;
    el.classList.add('is-touching');
    if (this.touchReleaseTimer) clearTimeout(this.touchReleaseTimer);
    this.updateTouchPos(ev, el);
  }

  onHeroTouchMove(ev: TouchEvent) {
    this.updateTouchPos(ev, ev.currentTarget as HTMLElement);
  }

  onHeroTouchEnd(ev: TouchEvent) {
    const el = ev.currentTarget as HTMLElement;
    // Hold the finger position for a beat before handing back to the orbit.
    this.touchReleaseTimer = setTimeout(() => {
      el.classList.remove('is-touching');
      el.style.removeProperty('--mx');
      el.style.removeProperty('--my');
    }, 1400);
  }

  private updateTouchPos(ev: TouchEvent, el: HTMLElement) {
    const t = ev.touches[0];
    if (!t) return;
    const rect = el.getBoundingClientRect();
    const mx = ((t.clientX - rect.left) / rect.width) * 100;
    const my = ((t.clientY - rect.top) / rect.height) * 100;
    el.style.setProperty('--mx', `${mx}%`);
    el.style.setProperty('--my', `${my}%`);
  }

  ngOnInit() {
    // Banners are handled by the lang-reactive effect() in the constructor.
    forkJoin({
      roots: this.api.getCached<Category[]>('/catalog/categories/roots/'),
      featured: this.api.getCached<Product[]>('/catalog/products/featured/'),
      bestsellers: this.api.getCached<Product[]>('/catalog/products/bestsellers/', { limit: 8 }),
      latest: this.api.getCached<Paginated<Product>>('/catalog/products/'),
      brands: this.api.getCached('/catalog/products/brands/'),
    }).subscribe(({ roots, featured, bestsellers, latest }) => {
      this.categories.set(roots || []);
      this.featured.set(featured || []);
      this.bestsellers.set(bestsellers || []);
      this.latest.set(latest.results?.slice(0, 8) || []);
    });

    for (const section of this.brandSections()) {
      this.api
        .getCached<Product[]>(`/catalog/products/by-brand/${encodeURIComponent(section.name)}/`, { limit: 4 })
        .subscribe((ps) => {
          this.brandSections.update((arr) =>
            arr.map((s) => (s.name === section.name ? { ...s, products: ps || [] } : s)),
          );
        });
    }
  }
}
