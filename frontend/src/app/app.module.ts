import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthService } from './modules/auth/auth.service';
import { AuthModule } from './modules/auth/auth.module';
import { HeaderComponent } from './shared/components/header/header.component';
import { AppPrimengModule } from './core/app-primeng.module';
import { UploadModule } from './modules/upload/upload.module';
import { CoreModule } from './core/core.module';
import { SharedModule } from './shared/shared.module';

@NgModule({
  declarations: [AppComponent],
  imports: [
    AuthModule,
    BrowserModule,
    AppRoutingModule,
    AppPrimengModule,
    UploadModule,
    CoreModule,
    SharedModule,
    BrowserAnimationsModule
  ],
  providers: [AuthService],
  bootstrap: [AppComponent, HeaderComponent]
})
export class AppModule {}
