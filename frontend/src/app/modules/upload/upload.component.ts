import { Component } from "@angular/core";
import { FileUploader } from "ng2-file-upload";

import { environment } from "app/../environments/environment";
import { UploadService } from "./upload.service";

@Component({
  selector: "app-upload",
  templateUrl: "./upload.component.html",
  styleUrls: ["./upload.component.styl"]
})
export class UploadComponent {
  public URL = environment.uploadUrl;
  public uploader: FileUploader;
  public hasBaseDropZoneOver: boolean = false;
  public showProgress: boolean = false;
  public wrongFile: boolean = false;
  public inputText: string;

  constructor(private uploadService: UploadService) {
    this.inputText = "";
    this.uploader = new FileUploader({
      url: this.URL,
      autoUpload: true,
      authToken: "test-user"
    });
    this.uploader.onAfterAddingFile = fileItem => {
      const fileName = fileItem.file.name;
      const isTxt = fileName.includes(".txt");
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
    };
  }

  private getExistingJobs(): { jobId: string; status: boolean }[] {
    const existingJobs = localStorage.getItem("jobs") || "[]";
    return JSON.parse(existingJobs);
  }

  private addToExistingJobs(jobId: string): void {
    const jobs = this.getExistingJobs();
    jobs.push({ jobId, status: false });
    localStorage.setItem("jobs", JSON.stringify(jobs));
  }

  public onProcessClick() {
    this.uploadService.processText(this.inputText).subscribe(resp => {
      if (resp.success) {
        const jobId = resp.data.jobId;
        this.addToExistingJobs(jobId);
      }
    });
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
