import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FlexLayoutModule } from '@angular/flex-layout';

import { SharedService } from 'app/shared/services/shared.service';
import { ApiService } from './services/api.service';
import { HeaderComponent } from './components/header/header.component';
import { AppPrimengModule } from 'app/core/app-primeng.module';

@NgModule({
  providers: [SharedService, ApiService],
  declarations: [HeaderComponent],
  imports: [
    CommonModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
    AppPrimengModule
  ],
  exports: [
    CommonModule,
    FlexLayoutModule,
    FormsModule,
    ReactiveFormsModule,
    HeaderComponent,
    AppPrimengModule
  ]
})
export class SharedModule {}
