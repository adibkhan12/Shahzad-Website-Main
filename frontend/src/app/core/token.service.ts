import { Injectable } from '@angular/core';

const ACCESS = 'sh_access';
const REFRESH = 'sh_refresh';
const GUEST = 'sh_guest_session';

@Injectable({ providedIn: 'root' })
export class TokenService {
  get access(): string | null { return localStorage.getItem(ACCESS); }
  get refresh(): string | null { return localStorage.getItem(REFRESH); }
  setTokens(access: string, refresh: string) {
    localStorage.setItem(ACCESS, access);
    localStorage.setItem(REFRESH, refresh);
  }
  clear() {
    localStorage.removeItem(ACCESS);
    localStorage.removeItem(REFRESH);
  }
  get guestSession(): string {
    let s = localStorage.getItem(GUEST);
    if (!s) {
      s = crypto.randomUUID();
      localStorage.setItem(GUEST, s);
    }
    return s;
  }
  clearGuestSession() { localStorage.removeItem(GUEST); }
}
