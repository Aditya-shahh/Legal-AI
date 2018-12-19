import { Component, OnInit, ViewChild } from '@angular/core';
import { RestService } from '../../shared/services/rest.service';
import { DashboardService } from './dashboard.service';
import {MatPaginator, MatTableDataSource} from '@angular/material';
import { NgxSpinnerService } from 'ngx-spinner';
import { SHARED_FORM_DIRECTIVES } from '@angular/forms/src/directives';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
    userQuery: String;
    caseList = [];
    showTable = false;
    error = false;
    emptyErr = false;
    show = false;

    // demoDataset = {
    //     "sentiment": {
    //         "document": {
    //          "score": -0.479108,
    //          "label": "negative"
    //         }
    //     },
    //     "emotion": {
    //         "document": {
    //             "emotion": {
    //                 "sadness": 0.494381,
    //                 "joy": 0.475491,
    //                 "fear": 0.088296,
    //                 "disgust": 0.127116,
    //                 "anger": 0.133539
    //             }
    //         }
    //     }
    // };


    constructor(private _rest: RestService, private dashboardService: DashboardService, private _spinner: NgxSpinnerService) {
    }

    displayedColumns: string[] = ['legal_id', 'case_body'];


  ngOnInit() {

  }


    submitForm() {
        this._spinner.show();

        if (this.userQuery !== undefined) {

            this.dashboardService.searchQuery(this.userQuery).subscribe(searchResult => {
                this._spinner.hide();
                console.log(searchResult);
                this.caseList = searchResult['summarized_search_result'];
                console.log(this.caseList);
                this.showTable = true;
                if (Object.keys(this.caseList).length === 0) {
                    this.showTable = false;
                    this.error = true;
                }
            }, err => {
                this._spinner.hide();
                console.log(err);
            });

        } else {
            this._spinner.hide();
            this.emptyErr = true;
        }

    }

    toggleShow(i) {
        console.log(i);
       // document.querySelector('div-' + i).style.cssText = "--my-var: #000"
        if ( document.getElementById(i).className.indexOf('show') > -1 ) {
            document.getElementById(i).classList.remove('show');
        } else {
            document.getElementById(i).classList.add('show');
        }
        this.show = true;

    }

}
