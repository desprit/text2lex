import { ApiResponse } from "./api.model";

export interface JobHistory {
  jobId: string;
  timestamp: number;
  relics: any[];
  success: boolean;
  nRelics: number;
  inProgress: boolean;
  sample: string;
  expired?: boolean;
}

export interface RelicTranslation {
  text: string;
  pos: string;
}

export interface Relic {
  lemma: string;
  example: string;
  translations: RelicTranslation[];
  i: number;
  idx: number;
  score: number;
}

export interface GetHistoryResponse extends ApiResponse {
  data?: JobHistory[];
}

export interface GetRelicsResponse extends ApiResponse {
  data?: Relic[];
}
