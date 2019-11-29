import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError, map } from "rxjs/operators";
import { of, Observable } from "rxjs";

import {
  LoginRequestPayload,
  LoginResponse
} from "app/shared/models/auth.model";
import { ApiResponse } from "app/shared/models/api.model";
import { ProcessTextResponse } from "../models/upload.model";
import { GetHistoryResponse, GetRelicsResponse } from "../models/history";

@Injectable({
  providedIn: "root"
})
export class ApiService {
  httpOptions: any;

  constructor(private httpClient: HttpClient) {
    this.httpOptions = {
      headers: new HttpHeaders({
        Authorization: "test-user"
      })
    };
  }

  public login(payload: LoginRequestPayload): Observable<LoginResponse> {
    return this.httpClient.post("login", payload).pipe(
      catchError(e => {
        console.error(e);
        return of({ success: false });
      }),
      map((response: any) => {
        return response;
      })
    );
  }

  public logout(): Observable<ApiResponse> {
    return this.httpClient.get("logout").pipe(
      catchError(e => {
        console.error(e);
        return of({ success: false });
      }),
      map((response: any) => {
        return response;
      })
    );
  }

  public processText(text: string): Observable<ProcessTextResponse> {
    return this.httpClient.post("upload", { text }, this.httpOptions).pipe(
      catchError(e => {
        console.error(e);
        return of({ success: false });
      }),
      map((response: any) => {
        return response;
      })
    );
  }

  public getHistory(): Observable<GetHistoryResponse> {
    return this.httpClient.get("history", this.httpOptions).pipe(
      catchError(e => {
        console.error(e);
        return of({ success: false });
      }),
      map((response: any) => {
        return response;
      })
    );
  }

  public getRelics(jobId: string): Observable<GetRelicsResponse> {
    return this.httpClient.get(`history/${jobId}`, this.httpOptions).pipe(
      catchError(e => {
        console.error(e);
        return of({ success: false });
      }),
      map((response: any) => {
        return response;
      })
    );
  }
}
