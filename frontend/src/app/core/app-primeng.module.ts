import { NgModule } from '@angular/core';
import { LayoutModule } from '@angular/cdk/layout';
import { CommonModule } from '@angular/common';
import { ToolbarModule } from 'primeng/toolbar';
import { CardModule } from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { MenuModule } from 'primeng/menu';
import { CheckboxModule } from 'primeng/checkbox';
import { TableModule } from 'primeng/table';
import { PaginatorModule } from 'primeng/paginator';
import { DropdownModule } from 'primeng/dropdown';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { DialogModule } from 'primeng/dialog';

@NgModule({
  providers: [],
  imports: [
    CommonModule,
    LayoutModule,
    ToolbarModule,
    CardModule,
    InputTextModule,
    ButtonModule,
    MenuModule,
    CheckboxModule,
    TableModule,
    PaginatorModule,
    DropdownModule,
    AutoCompleteModule,
    DialogModule
  ],
  exports: [
    LayoutModule,
    ToolbarModule,
    CardModule,
    InputTextModule,
    ButtonModule,
    MenuModule,
    CheckboxModule,
    TableModule,
    PaginatorModule,
    DropdownModule,
    AutoCompleteModule,
    DialogModule
  ]
})
export class AppPrimengModule {}
