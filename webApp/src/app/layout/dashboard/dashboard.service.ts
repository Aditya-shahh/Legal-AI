import { Injectable } from '@angular/core';
import { HttpClient, HttpParams,HttpHeaders } from '@angular/common/http';
import { Headers } from "@angular/http";
import { throwError } from "rxjs";
import { catchError, map, tap } from "rxjs/operators";




@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) { }


  searchQuery(search_string) {
    let opts;
    opts = {
        headers: this.getCommonHeaders(),
        params: new HttpParams().set('page', '0').set('search_string', search_string)
    }
    let search_url = "http://localhost:5000/api/search-case"
    return this.http.get(search_url, opts).pipe(
        map(res => {
            let searchResult = res;
            return searchResult;
        }),
        catchError(this.handleErrors)
    );
  }
  getCommonHeaders() {
    let headers = new HttpHeaders()
      .append('Content-Type', 'application/json')
    return headers;
  }
  handleErrors(error: Response) {
    return throwError(error);
  }

}
