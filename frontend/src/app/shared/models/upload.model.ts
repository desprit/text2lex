import { ApiResponse } from "./api.model";

export interface ProcessTextResponse extends ApiResponse {
  data?: {
    jobId: string;
  };
}
