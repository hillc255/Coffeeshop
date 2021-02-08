/* @TODO - Done:
 * Replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-mg9nhwma.us.auth0.com', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'fhaUZdOvVQ23tflbXrxAQ51HG7cXik2f', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // http://localhost:8100 https://127.0.0.1:8080/login-results the base url of the running ionic application. 
  }
};
