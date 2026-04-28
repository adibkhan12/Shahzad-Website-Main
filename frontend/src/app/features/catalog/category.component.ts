import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ApiService } from '../../core/api.service';
import { Category, Paginated, Product } from '../../core/models';
import { ProductCardComponent } from '../../shared/product-card.component';

@Component({
  selector: 'app-category',
  standalone: true,
  imports: [CommonModule, RouterLink, ProductCardComponent],
  template: `
    <div class="container-x py-12">
      <nav class="text-xs text-neutral-500 mb-6">
        <a routerLink="/" class="hover:text-ink transition">Home</a>
        <span class="mx-1.5">/</span>
        <a routerLink="/products" class="hover:text-ink transition">Shop</a>
        <span class="mx-1.5">/</span>
        <span class="text-ink">{{ category()?.name }}</span>
      </nav>
      <div class="eyebrow">Category</div>
      <h1 class="display text-4xl md:text-5xl mt-1 mb-10">{{ category()?.name }}</h1>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
        <app-product-card *ngFor="let p of products()" [product]="p" />
      </div>
    </div>
  `,
})
export class CategoryComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  category = signal<Category | null>(null);
  products = signal<Product[]>([]);

  ngOnInit() {
    this.route.paramMap.subscribe((p) => {
      const slug = p.get('slug')!;
      this.api.get<Category>(`/catalog/categories/${slug}/`).subscribe((c) => this.category.set(c));
      this.api
        .get<Paginated<Product>>('/catalog/products/', { category__slug: slug })
        .subscribe((r) => this.products.set(r.results || []));
    });
  }
}
