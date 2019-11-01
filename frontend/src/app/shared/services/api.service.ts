import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';
import { of, Observable } from 'rxjs';

import {
  LoginRequestPayload,
  LoginResponse
} from 'app/shared/models/auth.model';
import { ApiResponse } from 'app/shared/models/api.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private httpClient: HttpClient) {}

  public login(payload: LoginRequestPayload): Observable<LoginResponse> {
    return this.httpClient.post('login', payload).pipe(
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
    return this.httpClient.get('logout').pipe(
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
