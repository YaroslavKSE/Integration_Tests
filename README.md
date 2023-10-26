
---

# API and Tests

Implementing the API using the Flask module and tests using the `unittest` module in Python.

Visit [https://appforusers.top/](https://appforusers.top/) to use the API.

## Documentation of Available API Calls:

### 1. Online Users Statistics
- **Endpoint**: `/api/stats/users`
- **Description**: Get statistics about online users who were online at a specified time.
- **Parameters**:
  - `date`
  - `userId`

### 2. Retrieve User Predictions
- **Endpoint**: `/api/predictions/users`
- **Description**: Retrieve user predictions.
- **Parameters**:
  - `date`
  - `userId`
  - `tolerance`

### 3. Total User Statistics
- **Endpoint**: `/api/stats/user/total`
- **Description**: Get total statistics for a user.
- **Parameters**:
  - `date`
  - `averageRequired` (can be `true` or `false`)

### 4. User Forget Request
- **Endpoint**: `/api/user/forget`
- **Description**: Process a user forget request.
- **Parameters**:
  - `userId`

### 5. Reports by Name
- **Endpoint**: `/api/report/<report_name>`
- **Description**: Get or post a report by name.
- **Parameters**:
  - `from`
  - `to`

> Note: The name of the report should be specified by the user in the post request.

--- 
