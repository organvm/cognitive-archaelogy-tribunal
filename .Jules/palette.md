## 2024-05-23 - CLI Empty State Patterns
**Learning:**
Users often run a CLI tool without arguments to explore what it does. Showing a raw 'error: missing arguments' is hostile.
Implementing a 'Welcome Panel' for the empty state () significantly improves perceived quality and onboardability.
Using progressive enhancement (try/import) allows for beautiful UI when libraries like 'Rich' are available, while maintaining functionality (graceful degradation) when they are not.

**Action:**
Always check for empty arguments in CLI entry points and display a usage summary or dashboard instead of an error.
## 2024-05-23 - CLI Empty State Patterns
**Learning:**
Users often run a CLI tool without arguments to explore what it does. Showing a raw 'error: missing arguments' is hostile.
Implementing a 'Welcome Panel' for the empty state significantly improves perceived quality and onboardability.
Using progressive enhancement (try/import) allows for beautiful UI when libraries like 'Rich' are available, while maintaining functionality (graceful degradation) when they are not.

**Action:**
Always check for empty arguments in CLI entry points and display a usage summary or dashboard instead of an error.
