import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';

import { environment } from '../../environments/environment';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink, TranslateModule],
  template: `
    <footer class="mt-24 on-dark">
      <div class="container-x py-16">
        <div class="grid md:grid-cols-12 gap-10">
          <div class="md:col-span-5">
            <h2 class="display text-5xl md:text-6xl text-white tracking-tight leading-[0.95]">
              {{ 'footer.heading1' | translate }} <em>{{ 'footer.heading2' | translate }}</em>.
            </h2>
            <p class="mt-6 text-neutral-400 max-w-md">{{ 'footer.subtitle' | translate }}</p>
            <a [href]="'https://wa.me/' + whatsapp" target="_blank"
               class="mt-8 inline-flex items-center gap-2 text-sm text-white hover:text-brand-300 transition">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.194 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg>
              {{ 'footer.whatsappUs' | translate }}
            </a>
          </div>

          <div class="md:col-span-2">
            <h4 class="eyebrow text-neutral-500 mb-4">{{ 'footer.shop' | translate }}</h4>
            <ul class="space-y-2.5 text-sm">
              <li><a routerLink="/products" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.allProducts' | translate }}</a></li>
              <li><a routerLink="/products" [queryParams]="{category: 'smartphones'}" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.smartphones' | translate }}</a></li>
              <li><a routerLink="/products" [queryParams]="{category: 'laptops'}" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.laptops' | translate }}</a></li>
              <li><a routerLink="/products" [queryParams]="{category: 'audio'}" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.audio' | translate }}</a></li>
            </ul>
          </div>

          <div class="md:col-span-2">
            <h4 class="eyebrow text-neutral-500 mb-4">{{ 'footer.services' | translate }}</h4>
            <ul class="space-y-2.5 text-sm">
              <li><a routerLink="/repairs" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.repairServices' | translate }}</a></li>
              <li><a routerLink="/repairs/status" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.bookingStatus' | translate }}</a></li>
              <li><a routerLink="/orders/track" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.trackAnOrder' | translate }}</a></li>
            </ul>
          </div>

          <div class="md:col-span-3">
            <h4 class="eyebrow text-neutral-500 mb-4">{{ 'footer.company' | translate }}</h4>
            <ul class="space-y-2.5 text-sm">
              <li><a routerLink="/about" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.about' | translate }}</a></li>
              <li><a routerLink="/support" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.support' | translate }}</a></li>
              <li><a routerLink="/terms" class="link-underline text-neutral-400 hover:text-white">{{ 'footer.termsAndConditions' | translate }}</a></li>
            </ul>
          </div>
        </div>

        <div class="mt-16 pt-8 border-t border-white/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="text-xs text-neutral-500">© {{ year }} Shahzad Mobile &amp; Electronics. {{ 'footer.rights' | translate }}</div>
          <div class="flex items-center gap-3 text-xs text-neutral-500">
            <span>{{ 'footer.weAccept' | translate }}</span>
            <span class="px-2 py-1 rounded bg-white/5 border border-white/10">{{ 'footer.cashOnDelivery' | translate }}</span>
            <span class="px-2 py-1 rounded bg-white/5 border border-white/10">Tamara</span>
            <span class="px-2 py-1 rounded bg-white/5 border border-white/10">Tabby</span>
          </div>
        </div>
      </div>
    </footer>
  `,
})
export class FooterComponent {
  whatsapp = environment.whatsappNumber;
  year = new Date().getFullYear();
}
