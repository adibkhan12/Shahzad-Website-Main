import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { ApiService } from '../../core/api.service';
import { BrandGroup, Category, Paginated, Product } from '../../core/models';
import { ProductCardComponent } from '../../shared/product-card.component';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, FormsModule, ProductCardComponent, TranslateModule],
  template: `
    <div class="container-x pt-10 pb-20">
      <div class="mb-10">
        <div class="eyebrow">{{ 'productList.shop' | translate }}</div>
        <h1 class="display text-4xl md:text-5xl mt-1">{{ 'productList.allProducts' | translate }}</h1>
      </div>

      <div class="grid md:grid-cols-[240px_1fr] gap-10">
        <aside class="space-y-8 md:sticky md:top-24 h-fit">
          <div>
            <div class="eyebrow mb-3">{{ 'productList.category' | translate }}</div>
            <div class="space-y-1">
              <button (click)="setParam('category', '')"
                      [class.text-ink]="!category" [class.font-medium]="!category"
                      class="block text-sm text-neutral-500 hover:text-ink transition">{{ 'productList.allCategories' | translate }}</button>
              <button *ngFor="let c of categories()" (click)="setParam('category', c.slug)"
                      [class.text-ink]="category === c.slug" [class.font-medium]="category === c.slug"
                      class="block text-sm text-neutral-500 hover:text-ink transition">
                {{ c.name }}
              </button>
            </div>
          </div>
          <div>
            <div class="eyebrow mb-3">{{ 'productList.brand' | translate }}</div>
            <div class="space-y-0.5">
              <button (click)="setParam('brand', '')"
                      [class.text-ink]="!brand" [class.font-medium]="!brand"
                      class="block text-sm text-neutral-500 hover:text-ink transition">{{ 'productList.allBrands' | translate }}</button>
              <div *ngFor="let b of brands()">
                <button (click)="toggleBrand(b.name)"
                        [class.text-ink]="brand === b.name" [class.font-medium]="brand === b.name"
                        class="w-full flex items-center justify-between text-start text-sm text-neutral-500 hover:text-ink transition py-0.5">
                  <span>{{ b.name }}</span>
                  <span *ngIf="b.categories.length > 1"
                        class="text-[10px] text-neutral-400 transition-transform"
                        [class.rotate-180]="brand === b.name">▾</span>
                </button>
                <div *ngIf="brand === b.name && b.categories.length > 1"
                     class="ps-3 mt-1 mb-1.5 space-y-0.5 border-s border-neutral-200">
                  <button (click)="setParam('category', '')"
                          [class.text-ink]="!category" [class.font-medium]="!category"
                          class="block ps-2 text-xs text-neutral-500 hover:text-ink transition">{{ 'productList.allCategories' | translate }}</button>
                  <button *ngFor="let c of b.categories"
                          (click)="setParam('category', c.slug)"
                          [class.text-ink]="category === c.slug" [class.font-medium]="category === c.slug"
                          class="block ps-2 text-xs text-neutral-500 hover:text-ink transition">
                    {{ c.name }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <section>
          <div class="flex items-center gap-3 mb-6">
            <span class="text-sm text-neutral-500">{{ 'productList.count' | translate: { count: total() } }}</span>
            <select [ngModel]="sort" (ngModelChange)="setParam('sort', $event)"
                    class="ms-auto input !w-auto !py-2">
              <option value="">{{ 'productList.sortFeatured' | translate }}</option>
              <option value="price_asc">{{ 'productList.sortPriceAsc' | translate }}</option>
              <option value="price_desc">{{ 'productList.sortPriceDesc' | translate }}</option>
              <option value="name_asc">{{ 'productList.sortNameAsc' | translate }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
            <app-product-card *ngFor="let p of products()" [product]="p" />
          </div>
          <div *ngIf="!products().length" class="text-center py-20 text-neutral-500 text-sm">
            {{ 'productList.noMatch' | translate }}
          </div>
        </section>
      </div>
    </div>
  `,
})
export class ProductListComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  products = signal<Product[]>([]);
  categories = signal<Category[]>([]);
  brands = signal<BrandGroup[]>([]);
  total = signal(0);
  q = '';
  brand = '';        // holds the brand NAME (e.g. "Apple") — filters use brand__name
  sort = '';
  category = '';

  ngOnInit() {
    this.api.get<Category[]>('/catalog/categories/roots/').subscribe((c) => this.categories.set(c || []));
    this.route.queryParams.subscribe((p) => {
      this.q = p['q'] || '';
      this.brand = p['brand'] || '';
      this.sort = p['sort'] || '';
      this.category = p['category'] || '';
      this.reloadBrands();
      this.load();
    });
  }

  reloadBrands() {
    this.api.get<BrandGroup[]>('/catalog/products/brands/').subscribe((b) => this.brands.set(b || []));
  }

  load() {
    this.api
      .get<Paginated<Product>>('/catalog/products/', {
        q: this.q,
        brand__name: this.brand,
        sort: this.sort,
        category__slug: this.category,
      })
      .subscribe((r) => {
        this.products.set(r.results || []);
        this.total.set(r.count || 0);
      });
  }

  /** Toggle a brand in the sidebar: selecting a new brand clears the current
   *  category filter; re-clicking the active brand collapses it (clears filter). */
  toggleBrand(name: string) {
    if (this.brand === name) {
      this.router.navigate([], {
        queryParams: { brand: null, category: null },
        queryParamsHandling: 'merge',
      });
    } else {
      this.router.navigate([], {
        queryParams: { brand: name, category: null },
        queryParamsHandling: 'merge',
      });
    }
  }

  setParam(key: string, value: string) {
    this.router.navigate([], { queryParams: { [key]: value || null }, queryParamsHandling: 'merge' });
  }
}
