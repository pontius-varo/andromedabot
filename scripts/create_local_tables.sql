-- These are for SQLITE only! If you want to create these in another flavor of SQL, change the datatypes...
-- spreadsheet_cursor table
CREATE TABLE spreadsheet_cursor(row_start INTEGER, row_end INTEGER, modified DATETIME, id integer primary key);
-- error_log table
CREATE TABLE error_log(error TEXT, eventTime DATETIME, id integer primary key);