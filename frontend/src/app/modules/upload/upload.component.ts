import { Component } from '@angular/core';
import { FileUploader } from 'ng2-file-upload';

import { Router } from '@angular/router';
import { environment } from 'app/../environments/environment';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.styl']
})
export class UploadComponent {
  public URL = environment.uploadUrl;
  public uploader: FileUploader;
  public hasBaseDropZoneOver: boolean = false;
  public showProgress: boolean = false;
  public wrongFile: boolean = false;

  constructor(private router: Router) {
    this.uploader = new FileUploader({ url: this.URL, autoUpload: true });
    this.uploader.onAfterAddingFile = fileItem => {
      const fileName = fileItem.file.name;
      const isTxt = fileName.includes('.txt');
      if (!isTxt) {
        this.uploader.removeFromQueue(fileItem);
        this.wrongFile = true;
      } else {
        fileItem.withCredentials = false;
        this.wrongFile = false;
      }
    };
    this.uploader.onCompleteItem = fileItem => {
      this.showProgress = false;
      const fileName = fileItem.file.name;
      console.log(fileName);
    };
  }

  public fileOverBase(e: any): void {
    this.hasBaseDropZoneOver = e;
  }

  public onFileDrop() {
    if (this.wrongFile) {
      this.showProgress = false;
    } else {
      this.showProgress = true;
    }
  }
}
