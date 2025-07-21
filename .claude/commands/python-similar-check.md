---
name: python-similar-check
aliases: [pysimilar]
description: Find Python components with similar names
category: python
---

Find Python modules, classes, functions, or models with names similar to what you're looking for. Helps prevent creating duplicates with slightly different names.

This is an alias for `/python-exists-check` with similarity matching focus.

## Usage
```bash
/pysimilar [name]
```

## Examples
```bash
/pysimilar UserAuth
# Finds: UserAuthenticator, UserAuthService, AuthUser

/pysimilar DataProcessor
# Finds: DataProcessorBase, DataProcessorService, ProcessorData
```

See `/python-exists-check` for full documentation.
