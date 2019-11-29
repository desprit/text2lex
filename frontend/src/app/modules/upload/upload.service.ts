import { Injectable } from "@angular/core";
import { ApiService } from "app/shared/services/api.service";

@Injectable({
  providedIn: "root"
})
export class UploadService {
  constructor(private apiService: ApiService) {}

  public processText(text: string) {
    return this.apiService.processText(text);
  }
}
