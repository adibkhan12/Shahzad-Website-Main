import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthService } from './auth.service';
import { TokenService } from './token.service';

export const authGuard: CanActivateFn = (_route, state) => {
  const auth = inject(AuthService);
  const tokens = inject(TokenService);
  const router = inject(Router);
  if (auth.isAuthenticated() || tokens.access) return true;
  router.navigate(['/account/login'], { queryParams: { next: state.url } });
  return false;
};
