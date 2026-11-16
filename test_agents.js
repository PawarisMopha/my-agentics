import { StateGraph, Annotation } from "@langchain/langgraph";
import { generateText } from "ai";
import dotenv from "dotenv";

dotenv.config();

console.log("=== [1] Testing TypeScript / Node.js Agentic Stack ===");

// 1. Test LangGraph StateGraph definition
const State = Annotation.Root({
  messages: Annotation({
    reducer: (curr, update) => curr.concat(update),
    default: () => [],
  }),
});

const workflow = new StateGraph(State)
  .addNode("agent", (state) => ({
    messages: ["Node executed successfully"],
  }))
  .addEdge("__start__", "agent")
  .addEdge("agent", "__end__");

const app = workflow.compile();

async function runTest() {
  const result = await app.invoke({ messages: ["Hello Agent"] });
  console.log("✓ LangGraph StateGraph compiled and invoked:", result.messages);

  console.log("✓ Vercel AI SDK import validated (generateText function ready)");

  console.log("\nAll Node.js Agentic tests PASSED! ✨");
}

runTest().catch((err) => {
  console.error("Test failed:", err);
  process.exit(1);
});
