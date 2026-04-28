import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-static-page',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article class="container-x py-16 md:py-24 max-w-3xl">
      <div class="eyebrow">{{ page()?.title }}</div>
      <h1 class="display text-5xl md:text-6xl tracking-tight leading-[0.95] mt-4">{{ page()?.title }}</h1>
      <div class="mt-10 text-lg text-neutral-700 leading-relaxed whitespace-pre-wrap">{{ page()?.body }}</div>
    </article>
  `,
})
export class StaticPageComponent implements OnInit {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  page = signal<{ title: string; body: string } | null>(null);

  ngOnInit() {
    const slug = this.route.snapshot.data['slug'];
    this.api.get<{ title: string; body: string }>(`/core/pages/${slug}/`).subscribe((p) => this.page.set(p));
  }
}
