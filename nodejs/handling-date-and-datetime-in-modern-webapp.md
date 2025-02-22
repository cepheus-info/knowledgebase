# Handling Date and Datetime in Modern Webapp

## 1. Overview

In modern web applications, handling date and datetime is a common requirement. We need to distinguish between `date` and `datetime` and understand how to work with them in the frontend and backend.

## 2. Walkthrough

### 2.1. Concepts

#### 2.1.1. Date

A `Date` object represents a year-month-day in a calendar. It does not have a time component. For example, `2021-10-01` is a `Date`. The web application does not need to worry about the timezone when working with `Date`.

#### 2.1.2. Datetime

A `Datetime` object represents a specific instant in time with millisecond precision. It includes both the date and time components. For example, `2021-10-01T16:00:00Z` is a `Datetime`. The web application needs to consider the timezone when working with `Datetime`.

### 2.2. Problems

In legacy web applications, handling date and datetime can be tricky. Some common problems include:

#### 2.2.1. **Date stored in DATETIME**: In the database, the date is stored in a `DATETIME` column. When fetching the date, the time component is included, which may not be needed. Some databases do not have a separate `DATE` type. e.g., Oracle.

Consider the following date input in Browser: `1957-07-26`. When stored in a `DATETIME` column, it becomes `1957-07-25T15:00:00Z`. The time component is set to `15:00:00` in the database. We have different type to represent the same date in our application.

- **Store**

    | Target                   | Timezone/Offset | Equivalent Value     | Type                                           |
    | ------------------------ | --------------- | -------------------- | ---------------------------------------------- |
    | Browser (Asia/Hong_Kong) | GMT+09:00(DST)  | 1957-07-26T00:00:00  | Calendar UI Component (JavaScript Date Object) |
    | JSON Data                | UTC             | -392461200000        | Unix Timestamp                                 |
    | Java Backend             | UTC             | 1957-07-25T15:00:00Z | java.util.Date                                 |
    | SQL Parameter            | UTC             | 1957-07-25T15:00:00Z | java.sql.Date                                  |
    | Oracle Database          | UTC             | 1957-07-25T15:00:00Z | Oracle Date                                    |

- **Retrieve**

    This is the reverse process of storing the date.

    | Target                   | Timezone/Offset | Equivalent Value     | Type                                           |
    | ------------------------ | --------------- | -------------------- | ---------------------------------------------- |
    | Oracle Database          | UTC             | 1957-07-25T15:00:00Z | Oracle Date                                    |
    | SQL Result Set           | UTC             | 1957-07-25T15:00:00Z | java.sql.Date                                  |
    | Java Backend             | UTC             | 1957-07-25T15:00:00Z | java.util.Date                                 |
    | JSON Data                | UTC             | -392461200000        | Unix Timestamp                                 |
    | Browser (Asia/Shanghai)  | GMT+08:00       | 1957-07-25T23:00:00  | Calendar UI Component (JavaScript Date Object) |
    | Browser (Asia/Singapore) | GMT+07:30       | 1957-07-25T22:30:00  | Calendar UI Component (JavaScript Date Object) |
    | Browser (Asia/Hong_Kong) | GMT+09:00       | 1957-07-26T00:00:00  | Calendar UI Component (JavaScript Date Object) |

Consider the following date generated in Stored Procedure: `1900-01-01 00:00:00`. When it is returned to the Java Backend, it becomes `1899-12-31T16:00:00Z`. The time component is set to `16:00:00` in the Java Backend.

- **Retrieve**

    | Target                   | Timezone/Offset | Equivalent Value     | Type                                           |
    | ------------------------ | --------------- | -------------------- | ---------------------------------------------- |
    | Oracle Database          | GMT+08:00       | 1900-01-01T00:00:00  | Oracle Date                                    |
    | SQL Result Set           | UTC             | 1899-12-31T16:00:00Z | java.sql.Date                                  |
    | Java Backend             | UTC             | 1899-12-31T16:00:00Z | java.util.Date                                 |
    | JSON Data                | UTC             | -2209017600000       | Unix Timestamp                                 |
    | Browser (Asia/Shanghai)  | GMT+08:05       | 1900-01-01T00:05:43  | Calendar UI Component (JavaScript Date Object) |
    | Browser (Asia/Singapore) | GMT+06:55       | 1899-12-31T22:55:25  | Calendar UI Component (JavaScript Date Object) |
    | Browser (Asia/Hong_Kong) | GMT+07:36       | 1899-12-31T23:36:00  | Calendar UI Component (JavaScript Date Object) |

#### 2.2.2. **Timezone Conversion**: When working with datetime, we need to convert the timezone to display the datetime correctly. For example, `2021-10-01T16:00:00Z` in UTC needs to be converted to `2021-10-02 00:00:00` with respect to current Browser timezone.

### 2.3. Solutions

Considering the above problems, we can use the following approach to handle date and datetime in modern web applications:

1. **Use UTC**: Store and work with datetime in UTC timezone. 
   - For datetime: Convert the datetime to the Browser timezone when displaying it in the frontend.
   - For date: Ensure the UI component retrieve the date part of a UTC datetime, also create UTC date object while storing the date in backend. (This can be done by setting the time part to 00:00:00 while using UTC as the Component's timezone)
2. **Use Libraries**: Use libraries like `date-fns`, `moment.js`, or `Luxon` to handle date and datetime operations in the frontend.

Why?

- **Consistent**: Working with UTC ensures consistency across different timezones.
- **Compatibility**: Considering the Database might not have a separate `DATE` type, storing datetime in UTC is a common practice.