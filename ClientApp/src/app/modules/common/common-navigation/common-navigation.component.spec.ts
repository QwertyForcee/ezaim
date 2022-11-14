import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommonNavigationComponent } from './common-navigation.component';

describe('CommonNavigationComponent', () => {
  let component: CommonNavigationComponent;
  let fixture: ComponentFixture<CommonNavigationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommonNavigationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommonNavigationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
