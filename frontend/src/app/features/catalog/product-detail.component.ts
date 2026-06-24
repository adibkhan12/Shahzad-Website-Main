import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { CartService } from '../../core/cart.service';
import { Product, QA, Review } from '../../core/models';
import { ProductCardComponent } from '../../shared/product-card.component';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, ProductCardComponent, TranslateModule],
  template: `
    <div *ngIf="product() as p" class="container-x py-10">
      <!-- breadcrumb -->
      <nav class="text-xs text-neutral-500 mb-6">
        <a routerLink="/" class="hover:text-ink transition">{{ 'product.breadcrumbHome' | translate }}</a>
        <span class="mx-1.5">/</span>
        <a routerLink="/products" class="hover:text-ink transition">{{ 'product.breadcrumbShop' | translate }}</a>
        <span class="mx-1.5">/</span>
        <span class="text-ink">{{ p.title }}</span>
      </nav>

      <div class="grid md:grid-cols-2 gap-12">
        <!-- Gallery -->
        <div>
          <div class="relative aspect-square rounded-3xl bg-neutral-100 overflow-hidden">
            <img *ngIf="activeImage()" [src]="activeImage()" [alt]="p.title"
                 class="absolute inset-0 w-full h-full object-cover transition-opacity duration-500" />
            <span *ngIf="p.on_sale"
                  class="absolute top-4 start-4 px-3 py-1 text-[10px] uppercase tracking-wider bg-ink text-white rounded-full">{{ 'product.sale' | translate }}</span>
          </div>
          <div *ngIf="(p.images?.length || 0) > 1" class="flex gap-2.5 mt-4">
            <button *ngFor="let img of p.images" (click)="activeImage.set(img)"
                    class="w-16 h-16 rounded-xl overflow-hidden border-2 transition"
                    [class.border-ink]="activeImage()===img" [class.border-transparent]="activeImage()!==img">
              <img [src]="img" class="w-full h-full object-cover" />
            </button>
          </div>
        </div>

        <!-- Info -->
        <div class="md:pt-4">
          <div class="eyebrow">{{ p.brand?.name }}</div>
          <h1 class="display text-3xl md:text-5xl tracking-tight leading-tight mt-2">{{ p.title }}</h1>
          <div *ngIf="ratingCount() > 0" class="mt-3 flex items-center gap-2 text-sm text-neutral-600">
            <span class="text-amber-500">
              <ng-container *ngFor="let s of [1,2,3,4,5]">
                <span [class.opacity-25]="s > ratingAvg()">★</span>
              </ng-container>
            </span>
            <span>{{ ratingAvg().toFixed(1) }}</span>
            <span class="text-neutral-400">· {{ ratingCount() }} {{ 'product.reviews' | translate }}</span>
          </div>
          <div class="mt-6 flex items-baseline gap-3">
            <ng-container *ngIf="p.on_sale; else regularDetail">
              <span class="text-3xl font-semibold text-red-600">{{ p.sale_price }} {{ 'common.currency' | translate }}</span>
              <span class="line-through text-neutral-400">{{ p.price }}</span>
              <span class="chip !bg-red-50 !text-red-700">
                {{ 'product.save' | translate: { amount: (+p.price - +(p.sale_price || 0)).toFixed(0) } }}
              </span>
            </ng-container>
            <ng-template #regularDetail>
              <span class="text-3xl font-semibold">{{ p.price }} {{ 'common.currency' | translate }}</span>
            </ng-template>
          </div>
          <div class="mt-4 text-sm">
            <span *ngIf="p.stock > 0" class="inline-flex items-center gap-1.5 text-emerald-700">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              {{ 'product.shipsToday' | translate }}
            </span>
            <span *ngIf="p.stock === 0" class="text-red-600">{{ 'product.outOfStock' | translate }}</span>
          </div>
          <p class="mt-6 text-neutral-600 leading-relaxed">{{ p.description }}</p>

          <div class="mt-8 flex items-center gap-3">
            <div class="flex items-center border border-neutral-200 rounded-full overflow-hidden bg-white">
              <button (click)="qty = Math.max(1, qty-1)" class="w-10 h-11 text-neutral-500 hover:bg-neutral-50 hover:text-ink transition">−</button>
              <input type="number" [(ngModel)]="qty" min="1"
                     class="w-14 h-11 text-center border-0 focus:outline-none text-sm text-ink bg-transparent font-semibold tabular-nums" />
              <button (click)="qty = qty+1" class="w-10 h-11 text-neutral-500 hover:bg-neutral-50 hover:text-ink transition">+</button>
            </div>
            <button (click)="addToCart()" [disabled]="adding || p.stock === 0"
                    class="btn-primary flex-1 h-11 !rounded-full">
              {{ (adding ? 'product.adding' : 'product.addToCart') | translate }}
            </button>
          </div>
          <!--
          <div class="mt-6 grid grid-cols-3 gap-2 text-xs text-neutral-500">
            <div class="flex items-center gap-2"><span>🚚</span> {{ 'product.freeShipping' | translate }}</div>
            <div class="flex items-center gap-2"><span>🛡️</span> {{ 'product.warrantyShort' | translate }}</div>
            <div class="flex items-center gap-2"><span>↩️</span> {{ 'product.returnsShort' | translate }}</div>
          </div>
          -->
        </div>
      </div>

      <!-- Reviews & QA -->
      <div class="mt-20 grid md:grid-cols-2 gap-12">
        <section>
          <div class="eyebrow">{{ 'product.reviews' | translate }}</div>
          <h2 class="display text-2xl md:text-3xl mt-1 mb-6">{{ 'product.whatCustomersSay' | translate }}</h2>
          <div *ngIf="reviews().length === 0" class="text-sm text-neutral-500">{{ 'product.noReviews' | translate }}</div>
          <div *ngFor="let r of reviews()" class="py-5 border-b border-neutral-200/70 last:border-0">
            <div class="flex items-center gap-2 text-sm">
              <span class="font-medium">{{ r.user }}</span>
              <span class="text-amber-500 text-xs">
                <ng-container *ngFor="let s of [1,2,3,4,5]">
                  <span [class.opacity-25]="s > r.rating">★</span>
                </ng-container>
              </span>
            </div>
            <p class="mt-1.5 text-sm text-neutral-700">{{ r.text }}</p>
          </div>
          <form (ngSubmit)="submitReview()" class="mt-8 space-y-3">
            <div class="eyebrow">{{ 'product.leaveReview' | translate }}</div>
            <input [(ngModel)]="reviewForm.user" name="user" [placeholder]="'product.yourName' | translate" class="input" />
            <select [(ngModel)]="reviewForm.rating" name="rating" class="input">
              <option *ngFor="let n of [5,4,3,2,1]" [ngValue]="n">{{ 'product.stars' | translate: { count: n } }}</option>
            </select>
            <textarea [(ngModel)]="reviewForm.text" name="text" rows="3" [placeholder]="'product.yourReview' | translate" class="input"></textarea>
            <button class="btn-primary">{{ 'product.submitReview' | translate }}</button>
          </form>
        </section>

        <section>
          <div class="eyebrow">{{ 'product.questions' | translate }}</div>
          <h2 class="display text-2xl md:text-3xl mt-1 mb-6">{{ 'product.questionsAndAnswers' | translate }}</h2>
          <div *ngIf="qas().length === 0" class="text-sm text-neutral-500">{{ 'product.noQuestions' | translate }}</div>
          <div *ngFor="let q of qas()" class="py-5 border-b border-neutral-200/70 last:border-0">
            <div class="text-sm font-medium">{{ 'product.qLabel' | translate }} {{ q.question }}</div>
            <div class="text-xs text-neutral-500 mt-0.5">{{ 'product.askedBy' | translate: { name: q.user } }}</div>
            <div *ngIf="q.answer" class="mt-2 text-sm text-neutral-700">{{ 'product.aLabel' | translate }} {{ q.answer }}</div>
          </div>
          <form (ngSubmit)="submitQuestion()" class="mt-8 space-y-3">
            <div class="eyebrow">{{ 'product.askQuestion' | translate }}</div>
            <input [(ngModel)]="qaForm.user" name="user" [placeholder]="'product.yourName' | translate" class="input" />
            <textarea [(ngModel)]="qaForm.question" name="question" rows="2" [placeholder]="'product.yourQuestion' | translate" class="input"></textarea>
            <button class="btn-primary">{{ 'product.submitQuestion' | translate }}</button>
          </form>
        </section>
      </div>

      <!-- Related -->
      <section *ngIf="related().length" class="mt-20">
        <div class="eyebrow">{{ 'product.youMayAlsoLike' | translate }}</div>
        <h2 class="display text-2xl md:text-3xl mt-1 mb-6">{{ 'product.similarProducts' | translate }}</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          <app-product-card *ngFor="let r of related()" [product]="r" />
        </div>
      </section>
    </div>
  `,
})
export class ProductDetailComponent implements OnInit {
  private api = inject(ApiService);
  private cart = inject(CartService);
  private route = inject(ActivatedRoute);
  auth = inject(AuthService);
  Math = Math;

  product = signal<Product | null>(null);
  activeImage = signal<string>('');
  reviews = signal<Review[]>([]);
  qas = signal<QA[]>([]);
  related = signal<Product[]>([]);
  ratingAvg = signal(0);
  ratingCount = signal(0);
  qty = 1;
  adding = false;
  reviewForm = {
    user: 'Layla M.',
    rating: 5,
    text: 'Arrived the same day, exactly as described. Battery at 94%, no scratches, sealed in new packaging. Perfect experience.',
  };
  qaForm = {
    user: '',
    question: '',
  };

  ngOnInit() {
    this.route.paramMap.subscribe((p) => this.load(p.get('slug')!));
  }

  load(slug: string) {
    this.api.get<Product>(`/catalog/products/${slug}/`).subscribe((p) => {
      this.product.set(p);
      this.activeImage.set(p.primary_image || '');
      this.ratingAvg.set(p.rating_avg || 0);
      this.ratingCount.set(p.rating_count || 0);
    });
    this.api.get<Review[]>(`/catalog/products/${slug}/reviews/`).subscribe((r) => this.reviews.set(r || []));
    this.api.get<QA[]>(`/catalog/products/${slug}/qas/`).subscribe((q) => this.qas.set(q || []));
    this.api.get<Product[]>('/catalog/products/related/', { slug }).subscribe((r) => this.related.set(r || []));
  }

  addToCart() {
    const p = this.product();
    if (!p) return;
    this.adding = true;
    this.cart.add(p.id, this.qty).subscribe({
      next: () => (this.adding = false),
      error: () => (this.adding = false),
    });
  }

  submitReview() {
    const p = this.product();
    if (!p) return;
    this.api.post(`/catalog/products/${p.slug}/add_review/`, this.reviewForm).subscribe(() => {
      this.reviewForm = { user: '', rating: 5, text: '' };
      this.load(p.slug);
    });
  }

  submitQuestion() {
    const p = this.product();
    if (!p) return;
    this.api.post(`/catalog/products/${p.slug}/add_question/`, this.qaForm).subscribe(() => {
      this.qaForm = { user: '', question: '' };
      this.load(p.slug);
    });
  }
}
