import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { ApiService } from './api.service';
import { AuthResponse, User } from './models';
import { TokenService } from './token.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = inject(ApiService);
  private tokens = inject(TokenService);
  private router = inject(Router);

  readonly user = signal<User | null>(null);
  readonly isAuthenticated = computed(() => this.user() !== null);

  initFromStorage(): Observable<User> | null {
    if (!this.tokens.access) return null;
    const obs = this.api.get<User>('/accounts/me/');
    obs.subscribe({
      next: (u) => this.user.set(u),
      error: () => this.logout(false),
    });
    return obs;
  }

  login(email: string, password: string) {
    return this.api
      .post<AuthResponse>('/auth/login/', {
        email,
        password,
        session_key: this.tokens.guestSession,
      })
      .pipe(tap((r) => this.apply(r)));
  }

  register(data: any) {
    return this.api
      .post<AuthResponse>('/auth/register/', {
        ...data,
        session_key: this.tokens.guestSession,
      })
      .pipe(tap((r) => this.apply(r)));
  }

  google(idToken: string) {
    return this.api
      .post<AuthResponse>('/auth/google/', {
        id_token: idToken,
        session_key: this.tokens.guestSession,
      })
      .pipe(tap((r) => this.apply(r)));
  }

  private apply(r: AuthResponse) {
    this.tokens.setTokens(r.access, r.refresh);
    this.user.set(r.user);
    this.tokens.clearGuestSession();
  }

  logout(redirect = true) {
    this.tokens.clear();
    this.user.set(null);
    if (redirect) this.router.navigate(['/']);
  }

  refresh() {
    return this.api.post<{ access: string; refresh?: string }>('/auth/refresh/', {
      refresh: this.tokens.refresh,
    });
  }

  updateProfile(patch: Partial<User>) {
    return this.api.patch<User>('/accounts/me/', patch).pipe(tap((u) => this.user.set(u)));
  }
}
