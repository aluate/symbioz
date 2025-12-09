# Batch File Fix

## Issue
The batch file was getting "The system cannot find the path specified" errors because:
1. The `cd /d` command inside quoted strings wasn't working properly
2. Paths with spaces ("My Drive") needed better handling

## Solution
Changed from:
```bat
start "Title" cmd /k "cd /d "path" && command"
```

To:
```bat
pushd "path"
start "Title" cmd /k "command"
popd
```

This ensures:
- The directory change happens before starting the new window
- Paths with spaces are properly handled
- Each command runs in the correct directory

## Test It
Run `test_paths.bat` first to verify all paths exist, then try `start_otto_lifeos_mobile.bat` again.

