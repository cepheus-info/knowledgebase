# Application Architecture

## Components

We have hosted a Java Web Application in Azure App Service (Linux Tomcat Stack), which connect to Oracle Database running in On-Premise Data Center, the On-Premise Network exposed a public address/port to serve the Database connectivity.

The Java Web Application is packaged into a War file, which consists of a Servlet Backend, and a Static Diretory which provide a React Application.

The Java Backend also integrated with External PowerBI Reporting Server for Reporting Tasks.

The Java Backend also access Azure Key Vaults for Secret.

The Java Web Application uses Microsoft Entra ID for SSO.

We stream Application Logs to Azure Monitoring and Devo for Monitoring.

We collect metrics from Azure App Service to NewRelic for Alerts & Dashboard.

We make use of Jenkins Pipeline & BitBucket for DevOps and Git Repository.