import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthComponent } from './auth.component';
import { SharedModule } from 'app/shared/shared.module';
import { AuthService } from './auth.service';

@NgModule({
  providers: [AuthService],
  declarations: [AuthComponent],
  imports: [SharedModule, CommonModule],
  exports: [SharedModule]
})
export class AuthModule {}
