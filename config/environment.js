/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'euro-note',
    environment: environment,
    baseURL: '/',
    locationType: 'auto',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
  };

  ENV.contentSecurityPolicy = {
    'default-src' : "'none'",
    'font-src'    : "'self' http://code.ionicframework.com http://fonts.gstatic.com",
    'connect-src' : "'self'",
    'img-src'     : "'self' http://www.google-analytics.com/ https://s3.amazonaws.com data:",
    'style-src'   : "'self' 'unsafe-inline' http://fonts.gstatic.com http://fonts.googleapis.com http://code.ionicframework.com",
    'media-src'   : "'self'",
    'script-src'  : "'self' 'unsafe-eval' 'unsafe-inline' http://www.google-analytics.com/",
    'report-uri'  : "'none"
  }

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
