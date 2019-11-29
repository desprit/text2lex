import { Component, OnInit } from "@angular/core";

import { HistoryService } from "../history.service";
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: "app-dictionary",
  templateUrl: "./dictionary.component.html",
  styleUrls: ["./dictionary.component.styl"]
})
export class DictionaryComponent implements OnInit {
  constructor(
    public historyService: HistoryService,
    private activatedRoute: ActivatedRoute
  ) {}

  ngOnInit() {
    this.activatedRoute.params.subscribe(params => {
      const jobId = params.jobId;
      this.historyService.getRelics(jobId);
    });
  }

  public onDownloadClick(format: string) {
    console.log("Downloas as", format);
  }
}
