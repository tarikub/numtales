import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StoryServiceService {
  private apiUrl = '/api';
  private metURL = '/met';

  constructor(private http: HttpClient) {}

  public searchStory(query: string = ''): Observable<any> {
    const url = `${this.apiUrl}/searchstory?query=${encodeURIComponent(query)}`;
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.get<any>(url, httpOptions);
  }

  public searchImages(query: string = ''): Observable<any> {
    const url = `${this.apiUrl}/searchimage?query=${encodeURIComponent(query)}`;
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.get<any>(url, httpOptions);
  }

  public getStoryImage(objectId: string = ''): Observable<any> {
    const url = `${this.metURL}/${encodeURIComponent(objectId)}`;
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.get<any>(url, httpOptions);
  }
}
