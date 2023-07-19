# Patch a mongodb data

## Patch secondTasks

```json
// secondTasks[49].ceils
{
    "ceils": [
        {
            "id": "I_4763",
            "state": NumberInt("0")
        }
    ],
}
```

```json
// secondTasks[49].path[0][n]
{
    "id": "I_4763",
    "type": "stop",
    "mainTask": null,
    "secondTasks": {
        "qes": "I_4763",
        "taski": NumberInt("49"),
        "ceilsi": NumberInt("0")
    }
}
```

```json
// secondTasks[49].qes
{
  "qes": ["I_4763"]
}
```

```json
// totalData
{
    {
        "id": "I_4763",
        "type": "stop",
        "mainTask": null,
        "secondTasks": {
            "qes": "I_4763",
            "taski": NumberInt("49"),
            "ceilsi": NumberInt("0")
        }
    }
}
```
