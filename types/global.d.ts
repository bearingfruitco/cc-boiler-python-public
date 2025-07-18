declare global {
  interface Window {
    analytics?: {
      track: (event: string, properties?: any) => void;
      page: (name?: string, properties?: any) => void;
      identify: (userId: string, traits?: any) => void;
      load: (writeKey: string, dataPlaneUrl?: string) => void;
    };
    fbq?: (event: string, action: string, params?: any) => void;
    gtag?: (...args: any[]) => void;
    rudderanalytics?: any;
  }
}

export {};
