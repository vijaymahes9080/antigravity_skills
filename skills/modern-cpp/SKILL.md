---
name: modern-cpp
description: Idiomatic modern C++20 and C++23 engineering, RAII memory safety, smart pointers, ranges, concepts, CMake builds, and valgrind/ASan memory leak prevention.
---

# Modern C++ (C++20/C++23) Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Systems Programming & Software Development
- **Target Roles**: C/C++ Developer, Embedded Systems Engineer, High-Performance Computing Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "modern c++", "cpp20", "cpp23", "smart pointers", "raii", "cmake build", "memory leak fix cpp", "concepts and ranges".
- **Contextual Inferences**: Repositories containing `CMakeLists.txt`, `.cpp`, `.hpp`, `.h` files.
- **Chained Predecessors**: `task-decomposition`, `root-cause-debugging`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Writing pure C99/C11 code where C++ features are not supported by the toolchain.
  - Higher-level managed language tasks (Python, Java, TypeScript).

## 4. Required Inputs & Context
- C++ toolchain (GCC 12+, Clang 15+, MSVC 2022+ supporting C++20/C++23).
- Build system configuration (`CMakeLists.txt`).
- Memory sanitizer or debugger (AddressSanitizer, Valgrind).

## 5. Expected Outputs & Artifacts
- Type-safe, exception-safe C++ source code using RAII.
- Modern `CMakeLists.txt` using target-based commands (`target_include_directories`, `target_link_libraries`).
- Memory sanitization test report with zero leaks or use-after-free bugs.

## 6. Step-by-Step Operating Procedure
1. **Toolchain & Standard Verification**:
   - Verify compiler standard support: set `CMAKE_CXX_STANDARD 20` or `23`.
2. **Memory Safety & Resource Management (RAII)**:
   - Eliminate raw owning pointers (`new`/`delete`). Use `std::unique_ptr` for exclusive ownership and `std::shared_ptr`/`std::weak_ptr` for shared lifetimes.
3. **Concepts & Compile-Time Safety**:
   - Use C++20 `requires` clauses and concepts instead of verbose SFINAE template tricks.
4. **Modern Algorithms & Ranges**:
   - Replace raw for-loops with `std::ranges` algorithms and views for composable, non-owning transformations.
5. **Compilation & Sanitizer Validation**:
   - Compile with `-Wall -Wextra -Wpedantic -fsanitize=address,undefined`.

## 7. Repository Inspection & Planning Requirements
- Non-destructive CMake inspection:
  ```bash
  cmake --version
  grep -i "CMAKE_CXX_STANDARD" CMakeLists.txt
  ```
- Preservation rule: Preserve ABI compatibility where required; do not modify public C-linkage (`extern "C"`) signatures without explicit direction.

## 8. Tool & Dependency Requirements
- Modern C++ compiler, CMake 3.20+, Ninja or Make.
- Clang-Tidy, Clang-Format.

## 9. Implementation Guidelines & Best Practices
- Rule of Zero: Prefer classes that do not declare custom destructors, copy/move operations by relying on RAII members.
- Use `std::span` and `std::string_view` for zero-allocation parameter passing.
- Mark immutable functions `const` and compile-time constants `constexpr` or `consteval`.

```cpp
#include <memory>
#include <string_view>
#include <span>
#include <concepts>

template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

class ResourceHandler {
public:
    explicit ResourceHandler(std::string_view name) : resourceName_(name) {}
    
    [[nodiscard]] std::string_view getName() const noexcept {
        return resourceName_;
    }
private:
    std::string resourceName_;
};
```

## 10. Error Handling & Recovery Procedures
- Dangling reference with `std::string_view`: Ensure temporary strings outlive the string_view reference.
- Double-free crashes: Verify ownership semantics; never wrap the same raw pointer in two separate `std::unique_ptr`s.

## 11. Security & Privacy Constraints
- Prevent buffer overflows: Never use legacy unsafe functions (`strcpy`, `sprintf`, `gets`). Use bounds-checked alternatives or modern containers (`std::vector`, `std::array`).
- Mitigate use-after-free: Run AddressSanitizer (ASan) during CI test runs.

## 12. Verification & Testing Requirements
- Execute build and test:
  ```bash
  cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug -DENABLE_ASAN=ON
  cmake --build build --parallel
  ctest --test-dir build --output-on-failure
  ```

## 13. Completion Criteria
- Code compiles cleanly with zero warnings under `-Wall -Wextra`.
- AddressSanitizer and UndefinedBehaviorSanitizer report clean execution.
- All unit tests pass.

## 14. Relevant Official References
- ISO/IEC 14882:2020 (C++20 Standard).
- C++ Core Guidelines (Bjarne Stroustrup & Herb Sutter).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with modern GCC 13+, Clang 17+, MSVC 19.38+.
