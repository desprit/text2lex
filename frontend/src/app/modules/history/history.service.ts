import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { ApiService } from "app/shared/services/api.service";
import { JobHistory, Relic } from "app/shared/models/history";

@Injectable({
  providedIn: "root"
})
export class HistoryService {
  public jobs$: Observable<JobHistory[]>;
  public relics$: Observable<Relic[]>;

  constructor(private apiService: ApiService) {}

  public getHistory() {
    this.jobs$ = this.apiService.getHistory().pipe(map(resp => resp.data));
  }

  public getRelics(jobId: string) {
    this.relics$ = this.apiService
      .getRelics(jobId)
      .pipe(map(resp => resp.data));
  }
}
