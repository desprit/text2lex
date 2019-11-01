import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './modules/auth/auth.guard';
import { AuthComponent } from './modules/auth/auth.component';
import { UploadComponent } from './modules/upload/upload.component';

const routes: Routes = [
  {
    path: 'auth',
    component: AuthComponent
  },
  {
    path: 'upload',
    canActivate: [AuthGuard],
    component: UploadComponent
  },
  {
    path: '**',
    redirectTo: 'upload',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
