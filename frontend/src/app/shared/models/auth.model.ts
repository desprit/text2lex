import { ApiResponse } from './api.model';

export interface LoginRequestPayload {
  username: string;
  password: string;
}

export interface LoginResponse extends ApiResponse {
  data?: {
    role: string;
    token: string;
  };
}
