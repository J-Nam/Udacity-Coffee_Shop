/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'fsndrink.us', // the auth0 domain prefix
    audience: 'drinks', // the audience set for the auth0 app
    clientId: '2pd54HdaHepOK6ftyK7g3lnUUFj1fNVS', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
