# ClickUp Stories MCP - Test Scenarios

This document outlines comprehensive test scenarios for the ClickUp Stories MCP server and its associated skills.

## Environment Setup Test Scenarios

### TS-001: Environment Configuration
- **Scenario**: Verify all required environment variables are properly configured
- **Prerequisites**: `.env` file with valid ClickUp credentials
- **Test Steps**:
  1. Check `CLICKUP_API_TOKEN` is set and valid
  2. Verify `CLICKUP_TEAM_ID` exists and is accessible
  3. Confirm `CLICKUP_DEFAULT_LIST_ID` points to a valid list
- **Expected Result**: MCP server starts without authentication errors
- **Priority**: Critical
- **Status**: ✅ TESTED - PASSED (2025-12-17 09:55:46)
- **Results**:
  - ✓ CLICKUP_API_TOKEN: Set (44 chars, valid format)
  - ✓ CLICKUP_TEAM_ID: Set and accessible (19 spaces found)
  - ✓ CLICKUP_DEFAULT_LIST_ID: Set and properly formatted
  - ✓ API connectivity successful

### TS-002: API Connectivity
- **Scenario**: Test connection to ClickUp API
- **Test Steps**:
  1. Start MCP server
  2. Attempt to call `clickup_get_spaces` tool
- **Expected Result**: Returns list of available spaces
- **Priority**: Critical
- **Status**: ✅ TESTED - PASSED (2025-12-17 09:58:15)
- **Results**:
  - ✓ MCP server tool call successful
  - ✓ clickup_get_spaces tool executed correctly
  - ✓ Found 19 spaces in team
  - ✓ Response format valid with space names and IDs

## Core Functionality Test Scenarios

### TS-003: Basic Task Creation
- **Scenario**: Create a simple task with minimal required fields in NMEX Project Tracker list (6-901406617827-1)
- **Test Data**:
  ```json
  {
    "name": "Vitor's Test Task 1 - Basic Creation",
    "Platform": "iOS",
    "Priority": "Low",
    "Status": "ICEBOX",
    "Assignees": "Vitor Scarpinetti" 
  }
  ```
- **Test Steps**:
  1. Call `clickup_create_task` with task data
  2. Verify task is created in NMEX Project Tracker list (6-901406617827-1)
  3. Return the task and the ID
- **Expected Result**: Task created successfully with valid ID and URL
- **Status**: ✅ TESTED - PASSED (2025-12-17 10:43:53)
- **Results**:
  - ✓ Task created successfully in ClickUp
  - ✓ Task ID: 86b7w1guc
  - ✓ Task URL: https://app.clickup.com/t/86b7w1guc
  - ✓ Used list ID: 901406617827 (NMEX Project Tracker)
  - ✓ Priority: Low (converted from string "low" to integer 4)
  - ✓ Platform: iOS (custom field with option ID)
  - ✓ Status: ICEBOX (custom status fully supported)
  - ✓ Assignees: Vitor Scarpinetti (converted to user ID 96271408)
  - ✓ All test scenario fields now implemented and working
  - ✓ Server code updated with complete field mapping

### TS-004: Complete Task Creation
- **Scenario**: Create task with all available parameters
- **Test Data**:
  ```json
  {
    "name": "VITOR's Test Task - Complete",
    "description": "This is a **markdown** description with formatting",
    "status": "ICEBOX",
    "priority": 4,
    "tags": ["test", "automation", "mcp"],
    "custom_fields": {
      "field_id_123": "Custom Value"
    }
  }
  ```
- **Test Steps**:
  1. Get custom fields for target list
  2. Create task with all parameters
  3. Verify task details in ClickUp
- **Expected Result**: Task created with all specified attributes
- **Priority**: High

### TS-005: Task Creation with Custom List
- **Scenario**: Create task in specific list (not default)
- **Test Data**:
  ```json
  {
    "name": "Task in Custom List",
    "list_id": "custom_list_123"
  }
  ```
- **Test Steps**:
  1. Get available lists from a space
  2. Create task in specific list
- **Expected Result**: Task created in specified list
- **Priority**: High

## Data Retrieval Test Scenarios

### TS-006: Get All Spaces
- **Scenario**: Retrieve all spaces in the team
- **Test Steps**:
  1. Call `clickup_get_spaces`
  2. Verify response format and data
- **Expected Result**: List of spaces with names and IDs
- **Priority**: Medium

### TS-007: Get Lists from Space
- **Scenario**: Retrieve lists from a specific space
- **Test Data**: Valid space ID
- **Test Steps**:
  1. Get spaces to obtain valid space ID
  2. Call `clickup_get_lists` with space ID
- **Expected Result**: List of lists within the space
- **Priority**: Medium

### TS-008: Get Lists from Folder
- **Scenario**: Retrieve lists from a specific folder
- **Test Data**: Valid folder ID
- **Test Steps**:
  1. Call `clickup_get_lists` with folder ID
- **Expected Result**: List of lists within the folder
- **Priority**: Medium

### TS-009: Get Custom Fields
- **Scenario**: Retrieve custom fields for a list
- **Test Data**: Valid list ID
- **Test Steps**:
  1. Call `clickup_get_custom_fields` with list ID
  2. Verify field information
- **Expected Result**: List of custom fields with names, IDs, and types
- **Priority**: Medium

## Error Handling Test Scenarios

### TS-010: Invalid API Token
- **Scenario**: Test behavior with invalid API token
- **Test Steps**:
  1. Set invalid `CLICKUP_API_TOKEN`
  2. Attempt any API call
- **Expected Result**: Authentication error with clear message
- **Priority**: High

### TS-011: Missing Required Fields
- **Scenario**: Attempt task creation without required name field
- **Test Data**: `{}`
- **Test Steps**:
  1. Call `clickup_create_task` with empty parameters
- **Expected Result**: Validation error indicating missing name
- **Priority**: High

### TS-012: Invalid List ID
- **Scenario**: Create task with non-existent list ID
- **Test Data**:
  ```json
  {
    "name": "Test Task",
    "list_id": "invalid_list_123"
  }
  ```
- **Expected Result**: Error indicating list not found
- **Priority**: Medium

### TS-013: Invalid Priority Value
- **Scenario**: Use invalid priority value
- **Test Data**:
  ```json
  {
    "name": "Test Task",
    "priority": 5
  }
  ```
- **Expected Result**: Error or default priority applied
- **Priority**: Low

### TS-014: Malformed Custom Fields
- **Scenario**: Provide invalid custom field format
- **Test Data**:
  ```json
  {
    "name": "Test Task",
    "custom_fields": "invalid_format"
  }
  ```
- **Expected Result**: Error indicating invalid custom fields format
- **Priority**: Medium

## Integration Test Scenarios

### TS-015: MCP Server Lifecycle
- **Scenario**: Test server startup, operation, and shutdown
- **Test Steps**:
  1. Start MCP server
  2. Perform multiple operations
  3. Stop server gracefully
- **Expected Result**: Clean startup and shutdown without errors
- **Priority**: High

### TS-016: Concurrent Operations
- **Scenario**: Multiple simultaneous API calls
- **Test Steps**:
  1. Initiate multiple task creation requests simultaneously
  2. Verify all tasks are created correctly
- **Expected Result**: All operations complete successfully
- **Priority**: Medium

### TS-017: Rate Limiting Handling
- **Scenario**: Test behavior under ClickUp API rate limits
- **Test Steps**:
  1. Make rapid successive API calls
  2. Monitor for rate limit responses
- **Expected Result**: Graceful handling of rate limits
- **Priority**: Low

## Performance Test Scenarios

### TS-018: Large Description Handling
- **Scenario**: Create task with very large description
- **Test Data**: Task with 10KB+ markdown description
- **Expected Result**: Task created successfully without truncation
- **Priority**: Low

### TS-019: Bulk Operations
- **Scenario**: Create multiple tasks in sequence
- **Test Steps**:
  1. Create 10 tasks in quick succession
  2. Verify all tasks are created
- **Expected Result**: All tasks created without errors
- **Priority**: Medium

## Security Test Scenarios

### TS-020: Environment Variable Security
- **Scenario**: Verify API tokens are not logged or exposed
- **Test Steps**:
  1. Enable verbose logging
  2. Perform operations
  3. Check logs for exposed credentials
- **Expected Result**: No API tokens visible in logs
- **Priority**: Critical

### TS-021: Input Sanitization
- **Scenario**: Test with potentially malicious input
- **Test Data**:
  ```json
  {
    "name": "<script>alert('xss')</script>",
    "description": "'; DROP TABLE tasks; --"
  }
  ```
- **Expected Result**: Input properly escaped/sanitized
- **Priority**: High

## Edge Cases and Boundary Test Scenarios

### TS-022: Empty String Handling
- **Scenario**: Test with empty strings in various fields
- **Test Data**:
  ```json
  {
    "name": "Valid Task",
    "description": "",
    "tags": [""]
  }
  ```
- **Expected Result**: Appropriate handling of empty values
- **Priority**: Medium

### TS-023: Unicode and Special Characters
- **Scenario**: Create task with unicode and special characters
- **Test Data**:
  ```json
  {
    "name": "Task with émojis 🚀 and spéciál chärs",
    "description": "Testing unicode: 中文, العربية, русский"
  }
  ```
- **Expected Result**: Characters preserved correctly
- **Priority**: Medium

### TS-024: Maximum Field Length
- **Scenario**: Test behavior with very long field values
- **Test Data**: Task name with 500+ characters
- **Expected Result**: Appropriate handling (truncation or error)
- **Priority**: Low

## Workflow Test Scenarios

### TS-025: Complete Story Creation Workflow
- **Scenario**: End-to-end user story creation
- **Test Steps**:
  1. Get available spaces
  2. Get lists from selected space
  3. Get custom fields for target list
  4. Create story with appropriate fields
  5. Verify story in ClickUp interface
- **Expected Result**: Complete workflow executes successfully
- **Priority**: High

### TS-026: Multi-Environment Testing
- **Scenario**: Test with different ClickUp environments
- **Test Steps**:
  1. Test with different team configurations
  2. Verify behavior across environments
- **Expected Result**: Consistent behavior across environments
- **Priority**: Medium

## Test Data Management

### Test Environment Requirements
- ClickUp workspace with test team
- Multiple spaces and lists for testing
- Custom fields configured for testing
- Test API token with appropriate permissions

### Test Cleanup
- All test tasks should be tagged with "test-automation"
- Implement cleanup script to remove test data
- Document any permanent test data requirements

## Automation Guidelines

### Test Execution Order
1. Environment setup tests (TS-001, TS-002)
2. Core functionality tests (TS-003 to TS-009)
3. Error handling tests (TS-010 to TS-014)
4. Integration and performance tests (TS-015 to TS-019)
5. Security and edge case tests (TS-020 to TS-024)
6. Workflow tests (TS-025, TS-026)

### Success Criteria
- All Critical priority tests must pass
- 90% of High priority tests must pass
- Test execution time under 5 minutes
- No memory leaks or resource issues

### Reporting
- Generate detailed test reports with timestamps
- Include API response times and success rates
- Document any failing tests with debug information