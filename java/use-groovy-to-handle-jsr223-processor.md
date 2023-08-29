# Use groovy to handle JSR223 Processor

## 1. Groovy Script

```groovy
import groovy.json.JsonSlurper
import groovy.json.JsonOutput

import java.util.stream.Collectors

static void main(String[] args) {
    def jsonSlurper = new JsonSlurper()
    def jsonOutput = new JsonOutput()

    String data = """
    {
      "payload": [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        {"id": 3, "name": "Bob"}
      ]
    }
    """
    // String data = vars.get('data')
    def json = jsonSlurper.parseText(data)
    List<Object> payload = json.get('payload')

    def result = payload.stream().map {
        // return a new object literal
        return [
            propId: it.get('id'),
            propName: it.get('name')
        ]
    }.collect(Collectors.toList())

    println jsonOutput.toJson(result)
    // vars.put('result', jsonOutput.toJson(result))
}
```

## 2. Notice

- `vars` is a `Map` object, which is used to store variables in JMeter.

- `vars.get('result')` is used to get the result from `vars` object.

- `vars.put('result', jsonOutput.toJson(result))` is used to store the result in `vars` object.

- In groovy script, object literal is used to create a new object. The syntax is:

  ```groovy
  def obj = [
      prop1: 'value1',
      prop2: 'value2'
  ]
  ```

  The object literal is similar to the `Map` object in Java.

## 3. Conclusion

We demonstrate how to use groovy to handle JSR223 processor in JMeter. Which is very useful when we need to handle JSON data in JMeter.
