---
name: java-modern
description: Master Java 21+ and Java 25 modern features including Virtual Threads (Project Loom), Pattern Matching, Record patterns, Spring Boot 3.x, and high-throughput backend services.
---

# Modern Java (Java 21+) & Spring Boot Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Software Development & Enterprise Backend
- **Target Roles**: Java Developer, Backend Developer, Enterprise Systems Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "modern java", "java 21", "virtual threads loom", "spring boot 3", "record patterns java", "pattern matching java".
- **Contextual Inferences**: Repositories containing `pom.xml`, `build.gradle`, `build.gradle.kts` targeting Java 17+.
- **Chained Predecessors**: `task-decomposition`, `repo-audit`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Maintaining legacy Java 6/7/8 codebases with strict restrictions against upgrading language standards.
  - Client-side JavaScript/TypeScript or non-JVM languages.

## 4. Required Inputs & Context
- JDK 21+ (LTS).
- Build tool (Maven 3.9+ or Gradle 8+).
- Application framework descriptor (e.g. `spring-boot-starter-web`).

## 5. Expected Outputs & Artifacts
- Idiomatic Java 21+ code utilizing Records, Sealed Classes, and Pattern Matching.
- High-throughput concurrency services configured with Virtual Threads (`Executors.newVirtualThreadPerTaskExecutor()`).
- Automated JUnit 5 test suite with AssertJ and Mockito.

## 6. Step-by-Step Operating Procedure
1. **JDK & Toolchain Baseline**:
   - Verify Java runtime: `java --version` and check `maven.compiler.source` / `targetCompatibility` in build scripts.
2. **Data Modeling with Records & Sealed Interfaces**:
   - Replace verbose boilerplate POJOs with immutable `record` components.
   - Model finite domain states with `sealed interface` and `permits`.
3. **Concurrency & Virtual Threads**:
   - Configure Tomcat/Jetty in Spring Boot 3.2+ with `spring.threads.virtual.enabled=true`.
   - Avoid `synchronized` blocks that pin carrier threads; replace with `ReentrantLock`.
4. **Pattern Matching & Switch Expressions**:
   - Utilize exhaustive type matching without brittle `instanceof` casts.
5. **Testing & Performance Verification**:
   - Execute JUnit 5 tests and benchmark thread throughput.

## 7. Repository Inspection & Planning Requirements
- Non-destructive JDK and dependency inspection:
  ```bash
  java --version
  ./mvnw -v || gradle -v
  grep -A 2 "<java.version>" pom.xml || grep "jvmToolchain" build.gradle.kts
  ```
- Preservation rule: Avoid introducing third-party Lombok annotations when native Java records and pattern matching fulfill the requirement.

## 8. Tool & Dependency Requirements
- OpenJDK / Eclipse Temurin 21+, Maven or Gradle wrapper, JUnit 5.

## 9. Implementation Guidelines & Best Practices
- Never pool virtual threads (`newFixedThreadPool` on virtual threads is an anti-pattern). Let them be created and discarded per request.
- Use Structured Concurrency (`StructuredTaskScope`) for coordinating subtasks in parallel.

```java
public sealed interface OrderState permits Pending, Shipped, Cancelled {}
public record Pending(String orderId, double amount) implements OrderState {}
public record Shipped(String orderId, String trackingNumber) implements OrderState {}
public record Cancelled(String orderId, String reason) implements OrderState {}

public class OrderService {
    public String processState(OrderState state) {
        return switch (state) {
            case Pending(var id, var amt) -> "Order " + id + " pending for $" + amt;
            case Shipped(var id, var tracking) -> "Order " + id + " shipped: " + tracking;
            case Cancelled(var id, var reason) -> "Order " + id + " cancelled: " + reason;
        };
    }
}
```

## 10. Error Handling & Recovery Procedures
- Carrier Thread Pinning: If virtual threads freeze during blocking operations, check for `synchronized` statements calling blocking I/O; replace with `java.util.concurrent.locks.ReentrantLock`.

## 11. Security & Privacy Constraints
- Prevent XML External Entity (XXE) injection in XML parsers (`DocumentBuilderFactory`).
- Enforce strict parameter validation via Jakarta Validation (`@NotNull`, `@Size`, `@Email`).

## 12. Verification & Testing Requirements
- Run unit and integration tests:
  ```bash
  ./mvnw test || ./gradlew test
  ```
- Verify thread configuration:
  ```bash
  grep "spring.threads.virtual.enabled=true" src/main/resources/application.properties
  ```

## 13. Completion Criteria
- Code leverages Java 21+ features cleanly.
- Virtual thread configuration active without carrier thread pinning warnings.
- JUnit 5 test suite passes 100%.

## 14. Relevant Official References
- JEP 444: Virtual Threads (OpenJDK).
- JEP 440: Record Patterns & JEP 441: Pattern Matching for switch.
- Spring Boot 3.2+ Virtual Threads Reference.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Java 21 LTS and Java 25 preview builds.
