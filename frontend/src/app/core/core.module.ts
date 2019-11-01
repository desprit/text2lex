import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { SharedModule } from 'app/shared/shared.module';
import { ApiInterceptor } from './http-interceptor';

@NgModule({
  declarations: [],
  imports: [HttpClientModule, SharedModule],
  exports: [],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: ApiInterceptor, multi: true }
  ]
})
export class CoreModule {}
