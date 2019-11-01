import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <div fxLayout="column">
      <app-header></app-header>
      <div class="main">
        <router-outlet></router-outlet>
      </div>
    </div>
  `,
  styles: ['.main { min-height: calc(100vh - 64px); }']
})
export class AppComponent {
  title = 'Text2Lex';
}
