---
name: mcp-server-developer
description: Develop, debug, and publish Model Context Protocol (MCP) servers using TypeScript or Python SDKs. Implement Tools, Resources, Prompts, JSON-RPC 2.0 protocol handlers, stdio and SSE transports.
---

# Model Context Protocol (MCP) Server Engineering

## 1. Intended Role & Domain
- **Primary Domain**: AI Agent Tooling & Developer Productivity
- **Target Roles**: Developer Tooling Engineer, AI-Assisted Coding Specialist, Integration Architect
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "mcp server", "model context protocol", "build mcp tool", "mcp resources", "mcp prompts", "json-rpc agent tools", "connect mcp to antigravity".
- **Contextual Inferences**: Building custom tool bridges between external services (APIs, databases, internal CLIs) and AI agent systems (Antigravity, Claude Desktop).
- **Chained Predecessors**: `ai-agent-architect`, `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Building consumer web UI components without any AI tool or agent protocol integration.
  - Traditional monolithic REST APIs that have no MCP specification schema.

## 4. Required Inputs & Context
- Target service to expose (database, local filesystem, external SaaS API).
- MCP Transport type: `stdio` (standard input/output for local processes) or `sse` (Server-Sent Events for remote microservices).
- Implementation language: TypeScript/Node.js (`@modelcontextprotocol/sdk`) or Python (`mcp`).

## 5. Expected Outputs & Artifacts
- Production MCP Server implementation defining Tools, Resources, and Prompts.
- Strict input parameter schemas using JSON Schema / Zod / Pydantic.
- Configuration snippet for Antigravity (`mcp_config.json`) or client host.
- Integration test suite validating JSON-RPC protocol responses.

## 6. Step-by-Step Operating Procedure
1. **Server Initialization & Capabilities**:
   - Initialize the MCP `Server` instance with declared capabilities (`tools`, `resources`, `prompts`).
2. **Tool Definition & Schema Registration**:
   - Register tools with clear names, markdown descriptions explaining exact activation scenarios, and typed parameter schemas.
3. **Execution Handler Implementation**:
   - Implement handlers that validate arguments and return structured content arrays (`type: "text" | "image" | "resource"`).
4. **Transport Binding**:
   - Connect the server to `StdioServerTransport` for local subprocess communication or `SSEServerTransport` for HTTP streaming.
5. **Client Configuration & Validation**:
   - Register the server in `mcp_config.json` and verify discovery using the MCP Inspector tool.

## 7. Repository Inspection & Planning Requirements
- Non-destructive package check:
  ```bash
  cat package.json | grep -i "@modelcontextprotocol/sdk" 2>/dev/null || pip list | grep -i "mcp" 2>/dev/null || echo "MCP SDK not yet installed"
  ```
- Preservation rule: Never write debugging logs directly to `process.stdout` when using `stdio` transport; doing so corrupts the JSON-RPC message framing. Always use `process.stderr` for logging.

## 8. Tool & Dependency Requirements
- Node.js 18+ or Python 3.10+, `@modelcontextprotocol/sdk` or `mcp` Python package, `@modelcontextprotocol/inspector`.

## 9. Implementation Guidelines & Best Practices
- Every tool description must explain *what* it does, *why* to use it, and *when* to avoid it.
- Return error messages gracefully inside the MCP tool result (`isError: true`) instead of crashing the server process.

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

const server = new Server(
  { name: 'universal-mcp-bridge', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'query_system_metrics',
      description: 'Retrieve current CPU, memory, and disk utilization metrics.',
      inputSchema: {
        type: 'object',
        properties: {
          metricType: { type: 'string', enum: ['cpu', 'memory', 'disk', 'all'] },
        },
        required: ['metricType'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'query_system_metrics') {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ status: 'healthy', cpu_percent: 18.4, memory_free_mb: 4096 }),
        },
      ],
    };
  }
  throw new Error(`Tool not found: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## 10. Error Handling & Recovery Procedures
- Client drops connection: Handle SIGINT and SIGTERM gracefully to close open file descriptors and database pools.
- Invalid JSON-RPC request: Server returns standard JSON-RPC 2.0 error object (`code: -32600`, `message: "Invalid Request"`).

## 11. Security & Privacy Constraints
- Restrict filesystem access: Never expose tools that permit arbitrary unchrooted path traversal (`../../etc/passwd`).
- Protect API credentials: Load API keys via secure environment variables; never hardcode credentials into tool argument defaults.

## 12. Verification & Testing Requirements
- Test server using MCP Inspector:
  ```bash
  npx @modelcontextprotocol/inspector node dist/index.js
  ```
- Automated unit test: Send mock JSON-RPC string via stdin and assert valid JSON-RPC response via stdout.

## 13. Completion Criteria
- Server implements JSON-RPC 2.0 specification cleanly.
- Tools, resources, or prompts register with strict validation.
- Zero stdout pollution on stdio transport.

## 14. Relevant Official References
- Model Context Protocol Official Specification (modelcontextprotocol.io).
- Anthropic MCP Open Source Architecture.
- JSON-RPC 2.0 Specification.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with MCP Spec 2024-11-05 and 2025/2026 revisions.
