import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";

import { HistoryComponent } from "./history.component";
import { SharedModule } from "app/shared/shared.module";
import { HistoryService } from "./history.service";
import { DictionaryComponent } from './dictionary/dictionary.component';

@NgModule({
  providers: [HistoryService],
  declarations: [HistoryComponent, DictionaryComponent],
  imports: [SharedModule, CommonModule],
  exports: [SharedModule]
})
export class HistoryModule {}
