import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
    selector: 'app-topnav',
    templateUrl: './topnav.component.html',
    styleUrls: ['./topnav.component.scss']
})
export class TopnavComponent implements OnInit {

    constructor(public router: Router) {
    }

    ngOnInit() {
    }

    onLoggedout() {
        localStorage.removeItem('isLoggedin');
        this.router.navigate(['/login']);
    }

}
