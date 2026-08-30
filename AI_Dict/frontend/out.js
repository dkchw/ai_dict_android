(() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __require = /* @__PURE__ */ ((x) => typeof require !== "undefined" ? require : typeof Proxy !== "undefined" ? new Proxy(x, {
    get: (a, b) => (typeof require !== "undefined" ? require : a)[b]
  }) : x)(function(x) {
    if (typeof require !== "undefined") return require.apply(this, arguments);
    throw Error('Dynamic require of "' + x + '" is not supported');
  });
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));

  // src/components/ConversationTab.jsx
  var import_react = __toESM(__require("react"), 1);
  var import_lucide_react = __require("lucide-react");
  var import_react_markdown = __toESM(__require("react-markdown"), 1);
  var import_remark_gfm = __toESM(__require("remark-gfm"), 1);
  function ConversationTab({ tabId, fetchConversations, settings, models, onUpdateTab, initialConversation }) {
    const [conversationSearchTerm, setConversationSearchTerm] = (0, import_react.useState)(initialConversation ? initialConversation.text : "");
    const [conversationChats, setConversationChats] = (0, import_react.useState)([]);
    const [currentConversation, setCurrentConversation] = (0, import_react.useState)(initialConversation || null);
    const [loading, setLoading] = (0, import_react.useState)(false);
    const [chatInput, setChatInput] = (0, import_react.useState)("");
    const [editingChatId, setEditingChatId] = (0, import_react.useState)(null);
    const [editingContent, setEditingContent] = (0, import_react.useState)("");
    const [showConfig, setShowConfig] = (0, import_react.useState)(!initialConversation);
    const [config, setConfig] = (0, import_react.useState)({
      model: initialConversation?.model || settings.CONVERSATION_MODEL || settings.MAIN_MODEL || "~deepseek/deepseek-v4-flash-latest",
      thinking: initialConversation?.thinking || "none",
      memory_limit: initialConversation?.memory_limit || 20,
      system_prompt: initialConversation?.system_prompt || settings.CONVERSATION_PROMPT || ""
    });
    const chatEndRef = (0, import_react.useRef)(null);
    (0, import_react.useEffect)(() => {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [conversationChats]);
    (0, import_react.useEffect)(() => {
      if (initialConversation) {
        setLoading(true);
        fetch(`/api/conversations/${initialConversation.id}/chats`).then((res) => res.json()).then((d) => {
          setConversationChats(d.chats);
          setCurrentConversation(d.conversation);
          setConfig({
            model: d.conversation.model || config.model,
            thinking: d.conversation.thinking || config.thinking,
            memory_limit: d.conversation.memory_limit || config.memory_limit,
            system_prompt: d.conversation.system_prompt || config.system_prompt
          });
        }).catch((e) => console.error(e)).finally(() => setLoading(false));
      }
    }, [initialConversation]);
    (0, import_react.useEffect)(() => {
      let title = "New Conversation";
      if (conversationSearchTerm) title = conversationSearchTerm;
      if (currentConversation && !currentConversation.isTemp && currentConversation.text) title = currentConversation.text.substring(0, 30);
      onUpdateTab(tabId, { title, loading, hasData: !!currentConversation && !currentConversation.isTemp });
    }, [conversationSearchTerm, currentConversation, loading]);
    const updateConfigAPI = async (key, value) => {
      setConfig((prev) => ({ ...prev, [key]: value }));
      if (currentConversation && !currentConversation.isTemp) {
        await fetch(`/api/conversations/${currentConversation.id}/config`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ [key]: value })
        });
        setCurrentConversation((prev) => ({ ...prev, [key]: value }));
      }
    };
    const handleConversationSearch = async (e) => {
      e?.preventDefault();
      if (!conversationSearchTerm.trim()) return;
      setLoading(true);
      setCurrentConversation({ text: conversationSearchTerm, isTemp: true, ...config });
      setConversationChats([]);
      setShowConfig(false);
      try {
        const res = await fetch("/api/conversations/search", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: conversationSearchTerm,
            session_id: localStorage.getItem("active_session_id") || void 0,
            model: config.model,
            thinking: config.thinking,
            memory_limit: config.memory_limit,
            system_prompt: config.system_prompt
          })
        });
        if (!res.ok) throw new Error(await res.text());
        const d = await res.json();
        setConversationChats(d.chats);
        setCurrentConversation(d.conversation);
        setConfig({
          model: d.conversation.model || config.model,
          thinking: d.conversation.thinking || config.thinking,
          memory_limit: d.conversation.memory_limit || config.memory_limit,
          system_prompt: d.conversation.system_prompt || config.system_prompt
        });
        fetchConversations();
      } catch (err) {
        alert(err.message);
      } finally {
        setLoading(false);
      }
    };
    const handleChatSubmit = async (e) => {
      e?.preventDefault();
      if (!chatInput.trim() || !currentConversation || currentConversation.isTemp) return;
      const userMsg = { role: "user", content: chatInput, id: "temp-" + Date.now() };
      setConversationChats([...conversationChats, userMsg]);
      setChatInput("");
      setLoading(true);
      try {
        const res = await fetch(`/api/conversations/${currentConversation.id}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: userMsg.content })
        });
        if (!res.ok) throw new Error(await res.text());
        const d = await res.json();
        setConversationChats(d.chats);
      } catch (e2) {
        console.error(e2);
        alert(e2.message);
        setConversationChats((chats) => chats.filter((c) => c.id !== userMsg.id));
      } finally {
        setLoading(false);
      }
    };
    const handleSaveEdit = async (chatId) => {
      if (!editingContent.trim()) return;
      try {
        const res = await fetch(`/api/conversations/chats/${chatId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: editingContent })
        });
        if (res.ok) {
          setConversationChats((chats) => chats.map((c) => c.id === chatId ? { ...c, content: editingContent } : c));
          setEditingChatId(null);
        }
      } catch (e) {
        console.error(e);
      }
    };
    const handleDeleteChat = async (chatId) => {
      if (!confirm("Delete this message?")) return;
      try {
        const res = await fetch(`/api/conversations/chats/${chatId}`, { method: "DELETE" });
        if (res.ok) {
          setConversationChats((chats) => chats.filter((c) => c.id !== chatId));
        }
      } catch (e) {
        console.error(e);
      }
    };
    return /* @__PURE__ */ import_react.default.createElement("div", { className: "h-full flex flex-col max-w-5xl mx-auto w-full p-4 relative" }, !currentConversation || currentConversation.isTemp ? /* @__PURE__ */ import_react.default.createElement("form", { onSubmit: handleConversationSearch, className: "flex gap-2 mb-4" }, /* @__PURE__ */ import_react.default.createElement(
      "input",
      {
        type: "text",
        value: conversationSearchTerm,
        onChange: (e) => setConversationSearchTerm(e.target.value),
        placeholder: "Start a new conversation...",
        className: "flex-1 border dark:border-gray-600 dark:bg-gray-800 rounded-lg p-3 text-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
        disabled: loading
      }
    ), /* @__PURE__ */ import_react.default.createElement("button", { disabled: loading, type: "submit", className: "bg-blue-600 hover:bg-blue-700 transition-colors text-white px-6 rounded-lg font-medium flex items-center gap-2 disabled:opacity-50" }, loading ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin", size: 20 }) : /* @__PURE__ */ import_react.default.createElement(import_lucide_react.MessageSquare, { size: 20 }), /* @__PURE__ */ import_react.default.createElement("span", null, "Chat"))) : /* @__PURE__ */ import_react.default.createElement("div", { className: "flex justify-between items-center mb-4 bg-white dark:bg-gray-800 p-3 rounded-lg border dark:border-gray-700 shadow-sm" }, /* @__PURE__ */ import_react.default.createElement("h2", { className: "font-bold text-lg truncate max-w-[70%]" }, currentConversation.text), /* @__PURE__ */ import_react.default.createElement(
      "button",
      {
        onClick: () => setShowConfig(!showConfig),
        className: "flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      },
      /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Settings, { size: 16 }),
      "Config",
      showConfig ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.ChevronUp, { size: 16 }) : /* @__PURE__ */ import_react.default.createElement(import_lucide_react.ChevronDown, { size: 16 })
    )), showConfig && /* @__PURE__ */ import_react.default.createElement("div", { className: "mb-4 bg-white dark:bg-gray-800 p-4 rounded-xl border dark:border-gray-700 shadow-sm flex flex-col gap-3 transition-all" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex flex-col md:flex-row gap-4" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Model"), /* @__PURE__ */ import_react.default.createElement(
      "select",
      {
        value: config.model,
        onChange: (e) => updateConfigAPI("model", e.target.value),
        className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-sm"
      },
      /* @__PURE__ */ import_react.default.createElement("option", { value: "~deepseek/deepseek-v4-flash-latest" }, "v4-flash"),
      models.map((m) => /* @__PURE__ */ import_react.default.createElement("option", { key: m.id, value: m.id }, m.id))
    )), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Thinking Effort"), /* @__PURE__ */ import_react.default.createElement(
      "select",
      {
        value: config.thinking,
        onChange: (e) => updateConfigAPI("thinking", e.target.value),
        className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-sm"
      },
      /* @__PURE__ */ import_react.default.createElement("option", { value: "none" }, "None"),
      /* @__PURE__ */ import_react.default.createElement("option", { value: "enabled" }, "Enabled")
    )), /* @__PURE__ */ import_react.default.createElement("div", { className: "w-24" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Memory"), /* @__PURE__ */ import_react.default.createElement(
      "input",
      {
        type: "number",
        value: config.memory_limit,
        onChange: (e) => updateConfigAPI("memory_limit", parseInt(e.target.value) || 20),
        className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-sm"
      }
    ))), /* @__PURE__ */ import_react.default.createElement("div", null, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "System Prompt"), /* @__PURE__ */ import_react.default.createElement(
      "textarea",
      {
        value: config.system_prompt,
        onChange: (e) => updateConfigAPI("system_prompt", e.target.value),
        rows: "3",
        placeholder: "Custom instructions for this conversation...",
        className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500"
      }
    ))), currentConversation && !currentConversation.isTemp && /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1 overflow-y-auto mb-4 bg-white dark:bg-gray-800 rounded-xl border dark:border-gray-700 shadow-sm p-4" }, conversationChats.length === 0 && !loading && /* @__PURE__ */ import_react.default.createElement("div", { className: "h-full flex items-center justify-center text-gray-400" }, /* @__PURE__ */ import_react.default.createElement("p", null, "Conversation started. Send a message!")), /* @__PURE__ */ import_react.default.createElement("div", { className: "space-y-6" }, conversationChats.map((c, i) => /* @__PURE__ */ import_react.default.createElement("div", { key: c.id || i, className: `flex flex-col ${c.role === "user" ? "items-end" : "items-start"}` }, /* @__PURE__ */ import_react.default.createElement("div", { className: `max-w-[85%] md:max-w-[75%] rounded-xl overflow-hidden shadow-sm ${c.role === "user" ? "bg-blue-600 text-white" : "bg-gray-100 dark:bg-gray-900 border dark:border-gray-700"}` }, /* @__PURE__ */ import_react.default.createElement("div", { className: `flex justify-between items-center px-3 py-1.5 border-b ${c.role === "user" ? "bg-blue-700 border-blue-500" : "bg-gray-200 dark:bg-gray-800 border-gray-300 dark:border-gray-700"}` }, /* @__PURE__ */ import_react.default.createElement("span", { className: "font-bold text-xs opacity-80" }, c.role === "user" ? "You" : "AI"), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex gap-1" }, c.role === "user" && /* @__PURE__ */ import_react.default.createElement(import_react.default.Fragment, null, /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => {
      setEditingChatId(c.id);
      setEditingContent(c.content);
    }, className: "p-1 hover:bg-white/20 rounded transition-colors", title: "Edit message" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Pencil, { size: 12 })), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => handleDeleteChat(c.id), className: "p-1 hover:bg-white/20 rounded transition-colors", title: "Delete message" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Trash2, { size: 12 }))), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => {
      navigator.clipboard.writeText(c.content);
      alert("Copied!");
    }, className: "p-1 hover:bg-white/20 rounded transition-colors", title: "Copy message" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Copy, { size: 12 })))), /* @__PURE__ */ import_react.default.createElement("div", { className: "p-3 prose prose-sm dark:prose-invert max-w-none break-words" }, editingChatId === c.id ? /* @__PURE__ */ import_react.default.createElement("div", { className: "flex flex-col gap-2" }, /* @__PURE__ */ import_react.default.createElement("textarea", { value: editingContent, onChange: (e) => setEditingContent(e.target.value), className: "w-full bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border rounded p-2 text-sm focus:outline-none", rows: "3" }), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex justify-end gap-2" }, /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => setEditingChatId(null), className: "p-1.5 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-300 dark:hover:bg-gray-600" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.X, { size: 14 })), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => handleSaveEdit(c.id), className: "p-1.5 bg-green-500 text-white rounded hover:bg-green-600" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Check, { size: 14 })))) : /* @__PURE__ */ import_react.default.createElement(import_react_markdown.default, { remarkPlugins: [import_remark_gfm.default] }, c.content))))), loading && conversationChats.length > 0 && /* @__PURE__ */ import_react.default.createElement("div", { className: "flex items-start" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "bg-gray-100 dark:bg-gray-900 border dark:border-gray-700 p-3 rounded-xl rounded-tl-none" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin text-gray-400", size: 20 }))), /* @__PURE__ */ import_react.default.createElement("div", { ref: chatEndRef }))), currentConversation && !currentConversation.isTemp && /* @__PURE__ */ import_react.default.createElement("form", { onSubmit: handleChatSubmit, className: "flex gap-2" }, /* @__PURE__ */ import_react.default.createElement(
      "input",
      {
        type: "text",
        value: chatInput,
        onChange: (e) => setChatInput(e.target.value),
        placeholder: "Type your message...",
        className: "flex-1 border dark:border-gray-600 dark:bg-gray-800 rounded-lg p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
        disabled: loading
      }
    ), /* @__PURE__ */ import_react.default.createElement("button", { disabled: loading || !chatInput.trim(), type: "submit", className: "bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center justify-center" }, loading ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin", size: 20 }) : "Send")));
  }
})();
