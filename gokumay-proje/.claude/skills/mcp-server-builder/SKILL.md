---
name: mcp-server-builder
description: |
  MCP sunucu şablonları, araç tanımları, Termux kurulum.
  TypeScript ve Python MCP sunucu örnekleri.
  Kullan: "mcp-server-builder skill ile MCP kur"
---

# MCP Sunucu Oluşturma

## TOKEN KURALI
Tam sunucu kodu değil — araç şablonu + kurulum komutu.

---

## Minimum MCP Sunucu (TypeScript)

```typescript
// index.ts — Kopyala, araçları ekle, çalıştır
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const sunucu = new Server(
  { name: "gokumay-araclar", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

sunucu.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "araç_adı",
    description: "Ne yapar — Claude bunu okur",
    inputSchema: {
      type: "object",
      properties: {
        girdi: { type: "string", description: "Parametre açıklaması" }
      },
      required: ["girdi"]
    }
  }]
}));

sunucu.setRequestHandler(CallToolRequestSchema, async ({ params }) => {
  if (params.name === "araç_adı") {
    // İşlem yap
    return { content: [{ type: "text", text: `Sonuç: ${params.arguments?.girdi}` }] };
  }
  throw new Error(`Bilinmeyen araç: ${params.name}`);
});

await sunucu.connect(new StdioServerTransport());
```

---

## Kurulum (Termux)

```bash
# 1. Proje oluştur
mkdir -p ~/.claude/mcp-servers/gokumay-araclar
cd ~/.claude/mcp-servers/gokumay-araclar

# 2. Bağımlılıklar
npm init -y
npm install @modelcontextprotocol/sdk
npm install -g tsx  # TypeScript çalıştırıcı

# 3. Test
tsx index.ts

# 4. Claude Code'a ekle
claude mcp add gokumay-araclar \
  --transport stdio \
  -- tsx ~/.claude/mcp-servers/gokumay-araclar/index.ts

# 5. Doğrula
claude mcp list
```

---

## Hazır Araç Blokları (Kopyala-Yapıştır)

### Bash Çalıştırıcı
```typescript
{
  name: "bash_calistir",
  description: "Güvenli bash komutu çalıştır",
  inputSchema: {
    type: "object",
    properties: { komut: { type: "string" } },
    required: ["komut"]
  }
}
// Handler:
case "bash_calistir": {
  const { execSync } = await import("child_process");
  const cikti = execSync(params.arguments?.komut as string,
    { encoding: "utf8", timeout: 10000 });
  return { content: [{ type: "text", text: cikti }] };
}
```

### Dosya Okuyucu
```typescript
{
  name: "dosya_oku",
  description: "Dosya içeriğini oku",
  inputSchema: {
    type: "object",
    properties: { yol: { type: "string" } },
    required: ["yol"]
  }
}
// Handler:
case "dosya_oku": {
  const { readFileSync } = await import("fs");
  const icerik = readFileSync(params.arguments?.yol as string, "utf8");
  return { content: [{ type: "text", text: icerik.slice(0, 5000) }] };
}
```

### HTTP İstek
```typescript
{
  name: "api_cagir",
  description: "HTTP API çağrısı yap",
  inputSchema: {
    type: "object",
    properties: {
      url:    { type: "string" },
      metod:  { type: "string", enum: ["GET", "POST"] },
      govde:  { type: "object" }
    },
    required: ["url"]
  }
}
// Handler:
case "api_cagir": {
  const yanit = await fetch(params.arguments?.url as string, {
    method: params.arguments?.metod as string || "GET",
    headers: { "Content-Type": "application/json" },
    body: params.arguments?.govde
      ? JSON.stringify(params.arguments.govde) : undefined
  });
  const veri = await yanit.text();
  return { content: [{ type: "text", text: veri.slice(0, 3000) }] };
}
```

---

## Python MCP (Alternatif)

```python
# Termux'ta daha kolay kurulum
pip install mcp --break-system-packages

# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

app = Server("gokumay-python")

@app.list_tools()
async def araclar():
    return [types.Tool(
        name="hafiza_ara",
        description="Supabase'de ara",
        inputSchema={"type": "object",
                     "properties": {"sorgu": {"type": "string"}},
                     "required": ["sorgu"]}
    )]

@app.call_tool()
async def arac_calistir(name: str, arguments: dict):
    if name == "hafiza_ara":
        # Supabase araması yap
        sonuc = f"Aranan: {arguments['sorgu']}"
        return [types.TextContent(type="text", text=sonuc)]

async def main():
    async with stdio_server() as (okuma, yazma):
        await app.run(okuma, yazma, app.create_initialization_options())

import asyncio
asyncio.run(main())
```

```bash
# Claude Code'a Python MCP ekle
claude mcp add hafiza-arac \
  --transport stdio \
  -- python3 ~/.claude/mcp-servers/server.py
```
