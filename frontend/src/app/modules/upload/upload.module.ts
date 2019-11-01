import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileUploadModule } from 'ng2-file-upload';

import { UploadComponent } from './upload.component';
import { SharedModule } from 'app/shared/shared.module';
import { UploadService } from './upload.service';

@NgModule({
  providers: [UploadService],
  declarations: [UploadComponent],
  imports: [SharedModule, CommonModule, FileUploadModule],
  exports: [SharedModule],
  entryComponents: []
})
export class UploadModule {}
