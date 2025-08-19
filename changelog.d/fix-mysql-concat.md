- [Bugfix] Fixed an issue when syncing `credentials.core_user` to `openedx.auth_user` where the `full_name` field population failed with `ERROR 1292 (22007): Truncated incorrect DOUBLE value: 'FirstName'`.  
  MySQL does not support string concatenation with `+`, so it was incorrectly treated as a numeric operation. Updated to use `CONCAT()` for proper string concatenation.
