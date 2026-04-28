import { Routes } from '@angular/router';

import { authGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/catalog/home.component').then((m) => m.HomeComponent) },
  { path: 'products', loadComponent: () => import('./features/catalog/product-list.component').then((m) => m.ProductListComponent) },
  { path: 'products/:slug', loadComponent: () => import('./features/catalog/product-detail.component').then((m) => m.ProductDetailComponent) },
  { path: 'categories/:slug', loadComponent: () => import('./features/catalog/category.component').then((m) => m.CategoryComponent) },

  { path: 'cart', loadComponent: () => import('./features/cart/cart.component').then((m) => m.CartComponent) },

  { path: 'checkout', loadComponent: () => import('./features/checkout/checkout.component').then((m) => m.CheckoutComponent) },
  { path: 'checkout/return/:provider/:reference/:status', loadComponent: () => import('./features/checkout/return.component').then((m) => m.ReturnComponent) },

  { path: 'account/login', loadComponent: () => import('./features/account/login.component').then((m) => m.LoginComponent) },
  { path: 'account/register', loadComponent: () => import('./features/account/register.component').then((m) => m.RegisterComponent) },
  { path: 'account', canActivate: [authGuard], loadComponent: () => import('./features/account/dashboard.component').then((m) => m.DashboardComponent) },
  { path: 'account/addresses', canActivate: [authGuard], loadComponent: () => import('./features/account/addresses.component').then((m) => m.AddressesComponent) },

  { path: 'orders', canActivate: [authGuard], loadComponent: () => import('./features/orders/order-list.component').then((m) => m.OrderListComponent) },
  { path: 'orders/track', loadComponent: () => import('./features/orders/order-track.component').then((m) => m.OrderTrackComponent) },
  { path: 'orders/:reference', canActivate: [authGuard], loadComponent: () => import('./features/orders/order-detail.component').then((m) => m.OrderDetailComponent) },

  { path: 'repairs', loadComponent: () => import('./features/repairs/services.component').then((m) => m.RepairServicesComponent) },
  { path: 'repairs/status', loadComponent: () => import('./features/repairs/status.component').then((m) => m.RepairStatusComponent) },
  { path: 'repairs/book', loadComponent: () => import('./features/repairs/book.component').then((m) => m.RepairBookComponent) },
  { path: 'repairs/book/:slug', loadComponent: () => import('./features/repairs/book.component').then((m) => m.RepairBookComponent) },
  { path: 'repairs/confirm/:reference', loadComponent: () => import('./features/repairs/confirm.component').then((m) => m.RepairConfirmComponent) },

  { path: 'wishlist', canActivate: [authGuard], loadComponent: () => import('./features/wishlist/wishlist.component').then((m) => m.WishlistComponent) },

  { path: 'about', loadComponent: () => import('./features/pages/static-page.component').then((m) => m.StaticPageComponent), data: { slug: 'about' } },
  { path: 'terms', loadComponent: () => import('./features/pages/static-page.component').then((m) => m.StaticPageComponent), data: { slug: 'terms' } },
  { path: 'support', loadComponent: () => import('./features/pages/static-page.component').then((m) => m.StaticPageComponent), data: { slug: 'support' } },

  { path: '**', redirectTo: '' },
];
