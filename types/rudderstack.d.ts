export interface RudderAnalytics {
  load(writeKey: string, dataPlaneUrl: string): void;
  track(event: string, properties?: any): void;
  page(name?: string, properties?: any): void;
  identify(userId: string, traits?: any): void;
  reset(): void;
}

export interface RudderAnalyticsPreloader {
  [key: string]: any;
}

declare global {
  interface Window {
    rudderanalytics?: RudderAnalytics | RudderAnalyticsPreloader;
  }
}
