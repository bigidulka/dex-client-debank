const fs = require("fs");
const path = require("path");

const API_KEY = "cd387377-c201-4209-a1a0-0b969a4fecd2";
const USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36";
const modules = JSON.parse(fs.readFileSync(path.join(__dirname, "generated", "debank-signer-modules.json"), "utf8"));
const moduleCache = new Map();
const factories = new Map(Object.entries(modules).map(([id, source]) => [Number(id), new Function("module", "exports", "require", `return (${source})(module, exports, require);`)]));

const runtimeRequire = (id) => {
  if (moduleCache.has(id)) return moduleCache.get(id).exports;
  const factory = factories.get(id);
  if (!factory) throw new Error(`Module ${id} not found in extracted signer runtime`);
  const module = { exports: {} };
  moduleCache.set(id, module);
  factory(module, module.exports, runtimeRequire);
  return module.exports;
};
runtimeRequire.d = (exports, definition) => {
  for (const key of Object.keys(definition)) {
    if (!Object.prototype.hasOwnProperty.call(exports, key)) {
      Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
    }
  }
};
runtimeRequire.n = (module) => {
  const getter = () => module;
  getter.a = getter;
  return getter;
};
runtimeRequire.g = globalThis;

function randomId() {
  const alphabet = "abcdef0123456789";
  let result = "";
  for (let i = 0; i < 32; i += 1) result += alphabet[Math.floor(Math.random() * alphabet.length)];
  return result;
}

function signRequest(apiPath, params, method = "GET") {
  const previous = globalThis.__ggn;
  globalThis.__ggn = () => "debank.com";
  try {
    const signer = runtimeRequire(35653);
    const signed = signer.OK(params || {}, method, apiPath, { version: "v2" });
    return {
      "X-API-Key": API_KEY,
      "X-API-Time": String(Math.floor(Date.now() / 1000)),
      "x-api-ts": String(signed.ts),
      "x-api-nonce": signed.nonce,
      "x-api-ver": signed.version,
      "x-api-sign": signed.signature,
      "source": "web",
      "account": JSON.stringify({ random_at: Math.floor(Date.now() / 1000), random_id: randomId(), user_addr: null, connected_addr: null }),
      "referer": "https://debank.com/",
      "user-agent": USER_AGENT,
      "accept": "application/json",
    };
  } finally {
    globalThis.__ggn = previous;
  }
}

const payload = JSON.parse(process.argv[2] || "{}");
if (!payload.path || typeof payload.params !== "object") {
  throw new Error('Usage: node sign_headers.js "{\\"path\\":\\"/path\\",\\"params\\":{}}"');
}
process.stdout.write(JSON.stringify(signRequest(payload.path, payload.params, payload.method || "GET")));
