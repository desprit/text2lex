import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/components/common/menuitem';

import { AuthService } from 'app/modules/auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.styl']
})
export class HeaderComponent implements OnInit {
  public menuItems: MenuItem[];
  public navigationLinks: { icon: string; label: string; link: string }[];

  constructor(public authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.navigationLinks = [
      {
        link: 'upload',
        icon: 'pi-cloud-upload',
        label: 'Upload'
      },
      {
        link: 'howto',
        icon: 'pi-info',
        label: 'How to'
      }
    ];
    this.menuItems = [
      {
        label: 'Logout',
        command: (e: Event) => this.onLogoutClick(),
        disabled: !this.authService.loggedIn
      }
    ];
  }

  public onLogoutClick() {
    this.authService.logout();
  }

  public onLogoClick() {
    this.router.navigate(['database']);
  }

  public onLinkClick(pathName: string) {
    this.router.navigate([pathName]);
  }
}
