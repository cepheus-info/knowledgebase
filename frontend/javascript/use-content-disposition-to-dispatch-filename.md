# Use content-disposition to dispatch filename

## Problem

You want to use the `Content-Disposition` header to dispatch a filename to the browser.

If there are Unicode characters in your filename, then you will find your filename not working well.

## Solution

Use the `Content-Disposition` header to dispatch a filename to the browser.

```java
response.setHeader("Content-Disposition", "attachment; filename=\"hello.txt\"");
```

> Always use UrlEncoder to encode the filename.

```java
var filename = URLEncoder.encode("hello.txt", "UTF-8");
response.setHeader("Content-Disposition", "attachment; filename=\"" + filename + "\"");
```

## Discussion

The `Content-Disposition` header is used to tell the browser what to do with the content. It can be used to tell the browser to display the content inline, or to download the content as a file. The `Content-Disposition` header can also be used to specify the filename to use when downloading the content.

The `send_data` method takes an optional `:filename` parameter that can be used to specify the filename to use when downloading the content. The `send_file` method also takes an optional `:filename` parameter that can be used to specify the filename to use when downloading the content.

## See Also

- [RFC 2183](http://www.ietf.org/rfc/rfc2183.txt)
