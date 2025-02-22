# Troubleshooting Long Running Session-Destroying

## Problem

We have a Java Servlet application running in Azure App Service (Linux Tomcat Stack 9.0.96). The application uses Tomcat's standard Http Session. We found that the `sessionDestroyed` method is running for a long time. Which causes the application to be hanging for accepting new requests for a expiring session.

## Root Cause

The `sessionDestroyed` method is called when the session is invalidated or times out. We have two entrypoints to invoke the `sessionDestroyed` method:

1. Servlet Container: The servlet container calls the `sessionDestroyed` method when the session is invalidated or times out.
2. Application: The application will call the `session.invalidate()` method when doing the request.getSession() and the session is expired.

The `sessionDestroyed` method contains a synchronized block to prevent multiple threads from accessing the session at the same time. If the `sessionDestroyed` method is running for a long time, it means that the synchronized block is blocking other threads from accessing the session. Thus, the application is hanging.

## Solution

To solve the problem, we design a proactive approach to detect the long-running session-destroying. Once the session is started to be destroyed, we set an attribute (*expiring*) in the session to indicate that the session is being destroyed.

Once a subsequent request comes in, we have 2 scenarios:
1. If the Session has already been destroyed, we will get a new session directly and enter the application.

2. If the Session is still there and the *expiring* attribute is set, we reset client's session identifier via *Set-Cookie* and return a SessionExpiredException to the client. The client will be able to reload the page to get a new session.

### Implementation

Here's how you can implement resetting the client's session identifier using `Set-Cookie`:

```java
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

public class SessionManagementServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        
        if (session != null && session.getAttribute("expiring") != null) {
            // Determine the context path
            String contextPath = request.getContextPath();
            if (contextPath == null || contextPath.isEmpty()) {
                contextPath = "/";
            }
            
            // Reset the session identifier to empty and set HttpOnly and Secure attributes
            Cookie cookie = new Cookie("JSESSIONID", "");
            cookie.setPath(contextPath);
            cookie.setHttpOnly(true);
            cookie.setSecure(true);
            response.addCookie(cookie);
            
            // Throw SessionExpiredException to prompt the client to reload the page
            throw new SessionExpiredException("Session has expired. Please reload the page.");
        } else {
            // Normal processing
            // ...
        }
    }
    
    // Custom exception to handle session expiration
    public static class SessionExpiredException extends RuntimeException {
        public SessionExpiredException(String message) {
            super(message);
        }
    }
}
```
