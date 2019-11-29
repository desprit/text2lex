import { Router } from "@angular/router";
import { Component, OnInit, ViewEncapsulation } from "@angular/core";

import { HistoryService } from "./history.service";
import { JobHistory } from "app/shared/models/history";

@Component({
  selector: "app-history",
  templateUrl: "./history.component.html",
  styleUrls: ["./history.component.styl"],
  encapsulation: ViewEncapsulation.None
})
export class HistoryComponent implements OnInit {
  constructor(public historyService: HistoryService, private router: Router) {}

  ngOnInit() {
    this.historyService.getHistory();
  }

  public onJobClick(job: JobHistory) {
    this.router.navigate(["history", job.jobId]);
  }
}
