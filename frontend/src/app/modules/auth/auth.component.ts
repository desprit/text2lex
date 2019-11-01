import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

import { AuthService } from './auth.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.styl']
})
export class AuthComponent implements OnInit, OnDestroy {
  public valid: boolean = false;
  public username: string;
  public password: string;
  public usernameFormControl = new FormControl('', [Validators.required]);
  public passwordFormControl = new FormControl('', [Validators.required]);
  private destroy$: Subject<boolean> = new Subject();

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.usernameFormControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.checkFormValid();
      });
    this.passwordFormControl.valueChanges
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.checkFormValid();
      });
  }

  checkFormValid() {
    this.valid =
      this.usernameFormControl.valid && this.passwordFormControl.valid;
  }

  public onLoginClick() {
    if (!this.valid) {
      return;
    }
    const username = this.usernameFormControl.value;
    const password = this.passwordFormControl.value;
    const payload = { username, password };
    this.authService.login(payload);
  }

  ngOnDestroy() {
    this.destroy$.next(true);
  }
}
