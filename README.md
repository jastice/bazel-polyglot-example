# Bazel Polyglot Example

A single Bazel workspace demonstrating **Go**, **Scala**, **Python**, and **Kotlin** all built together with a unified `MODULE.bazel`.

## Structure

```
bazel-polyglot-example/
├── MODULE.bazel          # Unified Bazel module: rules_go, rules_scala, rules_python, rules_kotlin
├── BUILD.bazel           # Root build file
├── go/                   # Go services
│   ├── cmd/
│   │   ├── api_gateway/  # REST gateway using database + encryption + mathutil
│   │   ├── order_service/# Order processing with tax calculation
│   │   └── user_service/ # User registration service
│   └── pkg/
│       ├── database/     # In-memory DB with encrypted passwords
│       ├── encryption/   # ROT13 cipher + pseudo key generation
│       └── mathutil/     # Prime sieve + Fibonacci
├── scala/                # Scala stream-processing simulation
│   ├── analysis/         # Dependency graph & plan compiler
│   ├── apps/console/     # Console entry point
│   ├── common/           # Signal codec & temporal model
│   ├── domain/           # Service contracts & event model
│   ├── engine/           # Runtime & scheduler
│   └── simulation/lab/   # Scenario fabricator
├── python/               # Python calculator + text analyzer
│   ├── app/              # Main demo application
│   ├── libs/             # Math utils, string utils, datastructs, formatting
│   ├── services/         # Calculator engine & text analyzer
│   └── tests/            # Unit tests for all packages
└── kotlin/               # Kotlin matrix computation scheduler
    ├── app/              # Main entry point
    ├── core/             # Generic graph with topological sort
    ├── math/             # Matrix operations (addition, multiplication, transpose)
    └── utils/            # Job scheduler with thread pool
```

## Quick Start

```bash
# Build everything
bazel build //...

# Run Go binaries
bazel run //go/cmd/api_gateway
bazel run //go/cmd/order_service
bazel run //go/cmd/user_service

# Run Scala console
bazel run //scala/apps/console

# Run Python app
bazel run //python/app:main

# Run Kotlin app
bazel run //kotlin/app

# Run all tests
bazel test //...
```

## Languages & Rules

| Language | Bazel Rule Set     | Version   |
|----------|--------------------|-----------|
| Go       | `rules_go`         | 0.60.0    |
| Scala    | `rules_scala`      | 7.2.4     |
| Python   | `aspect_rules_py`  | 1.11.2    |
| Kotlin   | `rules_kotlin`     | 2.3.20    |

All languages share the same Bazel version (`9.0.2`) and are configured in a single `MODULE.bazel`.
