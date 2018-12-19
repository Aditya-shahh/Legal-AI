import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor( private _http: HttpClient,
                private _router: Router
              ) { }


  public sendLegalData(data) {


    const url = environment.ip + '/case_search';

    return this._http.get(url);

  }

}
