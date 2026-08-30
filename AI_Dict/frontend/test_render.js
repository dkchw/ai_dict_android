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

  // ../test_render.jsx
  var import_react2 = __toESM(__require("react"));
  var import_server = __require("react-dom/server");

  // src/components/CorrectionTab.jsx
  var import_react = __toESM(__require("react"), 1);
  var import_lucide_react = __require("lucide-react");
  var import_react_markdown = __toESM(__require("react-markdown"), 1);
  var import_remark_gfm = __toESM(__require("remark-gfm"), 1);
  function CorrectionTab({ tabId, fetchCorrections, settings, models, onUpdateTab, initialCorrection }) {
    const [correctionSearchTerm, setCorrectionSearchTerm] = (0, import_react.useState)(initialCorrection ? initialCorrection.text : "");
    const [correctionChats, setCorrectionChats] = (0, import_react.useState)([]);
    const [currentCorrection, setCurrentCorrection] = (0, import_react.useState)(initialCorrection || null);
    const [loading, setLoading] = (0, import_react.useState)(false);
    const [chatInput, setChatInput] = (0, import_react.useState)("");
    const [editingChatId, setEditingChatId] = (0, import_react.useState)(null);
    const [editingContent, setEditingContent] = (0, import_react.useState)("");
    const [showConfig, setShowConfig] = (0, import_react.useState)(!initialCorrection);
    const [localTitle, setLocalTitle] = (0, import_react.useState)(initialCorrection ? (initialCorrection.text || "").substring(0, 30) : "New Document");
    const [config, setConfig] = (0, import_react.useState)({
      model: initialCorrection?.model || settings.CORRECTION_MODEL || settings.MAIN_MODEL || "~deepseek/deepseek-v4-flash-latest",
      thinking: initialCorrection?.thinking || "none",
      memory_limit: initialCorrection?.memory_limit || 20,
      system_prompt: initialCorrection?.system_prompt || settings.CORRECTION_PROMPT || ""
    });
    const chatEndRef = (0, import_react.useRef)(null);
    (0, import_react.useEffect)(() => {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [correctionChats]);
    (0, import_react.useEffect)(() => {
      if (initialCorrection) {
        setLoading(true);
        fetch(`/api/corrections/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: initialCorrection.text })
        }).then((res) => res.json()).then((d) => {
          setCorrectionChats(d.chats || []);
          setCurrentCorrection(d.correction);
          if (d.correction) {
            setConfig({
              model: d.correction.model || config.model,
              thinking: d.correction.thinking || config.thinking,
              memory_limit: d.correction.memory_limit || config.memory_limit,
              system_prompt: d.correction.system_prompt || config.system_prompt
            });
            if (d.correction.text) setLocalTitle((d.correction.text || "").substring(0, 30));
          }
        }).catch((e) => console.error(e)).finally(() => setLoading(false));
      }
    }, [initialCorrection]);
    (0, import_react.useEffect)(() => {
      let title = localTitle;
      if (currentCorrection && !currentCorrection.isTemp && currentCorrection.text) title = (currentCorrection.text || "").substring(0, 30);
      onUpdateTab(tabId, { title, loading, hasData: !!currentCorrection && !currentCorrection.isTemp });
    }, [localTitle, currentCorrection, loading]);
    const updateConfigAPI = async (key, value) => {
      setConfig((prev) => ({ ...prev, [key]: value }));
      if (currentCorrection && !currentCorrection.isTemp) {
        await fetch(`/api/corrections/${currentCorrection.id}/config`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ [key]: value })
        });
        setCurrentCorrection((prev) => ({ ...prev, [key]: value }));
      }
    };
    const handleInitialSubmit = async (customPrompt = null) => {
      if (!correctionSearchTerm.trim()) return;
      setLoading(true);
      const promptToUse = customPrompt ? customPrompt + "\n\n" + config.system_prompt : config.system_prompt;
      setCurrentCorrection({ text: correctionSearchTerm, isTemp: true, ...config });
      setCorrectionChats([]);
      setShowConfig(false);
      try {
        const res = await fetch("/api/corrections/search", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: correctionSearchTerm,
            session_id: localStorage.getItem("active_session_id") || void 0,
            model: config.model,
            thinking: config.thinking,
            memory_limit: config.memory_limit,
            system_prompt: promptToUse
          })
        });
        if (!res.ok) throw new Error(await res.text());
        const d = await res.json();
        setCorrectionChats(d.chats || []);
        setCurrentCorrection(d.correction);
        if (d.correction) {
          setConfig({
            model: d.correction.model || config.model,
            thinking: d.correction.thinking || config.thinking,
            memory_limit: d.correction.memory_limit || config.memory_limit,
            system_prompt: d.correction.system_prompt || config.system_prompt
          });
        }
        fetchCorrections();
      } catch (err) {
        alert(err.message);
      } finally {
        setLoading(false);
      }
    };
    const handleChatSubmit = async (e, directMessage = null) => {
      e?.preventDefault();
      const contentToSend = directMessage || chatInput;
      if (!contentToSend.trim() || !currentCorrection || currentCorrection.isTemp) return;
      const userMsg = { role: "user", content: contentToSend, id: "temp-" + Date.now() };
      setCorrectionChats([...correctionChats, userMsg]);
      if (!directMessage) setChatInput("");
      setLoading(true);
      try {
        const res = await fetch(`/api/corrections/chats`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ correction_id: currentCorrection.id, content: userMsg.content })
        });
        if (!res.ok) throw new Error(await res.text());
        const d = await res.json();
        setCorrectionChats(d.chats || []);
      } catch (e2) {
        console.error(e2);
        alert(e2.message);
        setCorrectionChats((chats) => chats.filter((c) => c.id !== userMsg.id));
      } finally {
        setLoading(false);
      }
    };
    const handleSaveEdit = async (chatId) => {
      if (!editingContent.trim()) return;
      try {
        const res = await fetch(`/api/corrections/chats/${chatId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: editingContent })
        });
        if (res.ok) {
          setCorrectionChats((chats) => chats.map((c) => c.id === chatId ? { ...c, content: editingContent } : c));
          setEditingChatId(null);
        }
      } catch (e) {
        console.error(e);
      }
    };
    const handleDeleteChat = async (chatId) => {
      if (!confirm("Delete this message?")) return;
      try {
        const res = await fetch(`/api/corrections/chats/${chatId}`, { method: "DELETE" });
        if (res.ok) {
          setCorrectionChats((chats) => chats.filter((c) => c.id !== chatId));
        }
      } catch (e) {
        console.error(e);
      }
    };
    const PRESETS = [
      { label: "Grammar", prompt: "Please correct only the grammar, spelling, and punctuation of the text. Do not rewrite or change the tone." },
      { label: "Academic", prompt: "Please rewrite the text to be highly academic, formal, structured, and objective." },
      { label: "Natural", prompt: "Please rewrite the text so it sounds completely natural, fluent, and conversational to a native speaker." },
      { label: "Professional", prompt: "Please rewrite the text to be professional, polite, concise, and suitable for business communication." }
    ];
    return /* @__PURE__ */ import_react.default.createElement("div", { className: "h-full flex flex-col xl:flex-row w-full bg-gray-50 dark:bg-gray-950" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1 flex flex-col border-r dark:border-gray-800 p-4 min-w-[50%] h-[50vh] xl:h-full" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex items-center justify-between mb-4" }, /* @__PURE__ */ import_react.default.createElement(
      "input",
      {
        type: "text",
        value: currentCorrection && !currentCorrection.isTemp ? (currentCorrection.text || "").substring(0, 50) : localTitle,
        onChange: (e) => setLocalTitle(e.target.value),
        disabled: !!currentCorrection && !currentCorrection.isTemp,
        placeholder: "Document Title",
        className: "font-bold text-xl bg-transparent border-none focus:outline-none focus:ring-0 w-full truncate text-gray-900 dark:text-gray-100"
      }
    ), currentCorrection && !currentCorrection.isTemp && /* @__PURE__ */ import_react.default.createElement("button", { onClick: async () => {
      setLoading(true);
      await fetch(`/api/corrections/${currentCorrection.id}/generate-title`, { method: "POST" });
      fetchCorrections();
      setLoading(false);
    }, className: "text-gray-400 hover:text-gray-700 dark:hover:text-gray-200", title: "Auto Generate Title" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Sparkles, { size: 18 }))), /* @__PURE__ */ import_react.default.createElement(
      "textarea",
      {
        value: correctionSearchTerm,
        onChange: (e) => setCorrectionSearchTerm(e.target.value),
        placeholder: "Paste or type your text here to be corrected or improved...",
        className: "flex-1 w-full bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-xl p-4 shadow-inner resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm text-gray-900 dark:text-gray-100",
        disabled: loading || !!currentCorrection && !currentCorrection.isTemp
      }
    ), !currentCorrection || currentCorrection.isTemp ? /* @__PURE__ */ import_react.default.createElement("div", { className: "mt-4 flex flex-wrap gap-2" }, /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => handleInitialSubmit(), disabled: loading, className: "bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 disabled:opacity-50 transition-colors" }, loading ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin", size: 16 }) : /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Wand2, { size: 16 }), "Default Correct"), PRESETS.map((p) => /* @__PURE__ */ import_react.default.createElement("button", { key: p.label, onClick: () => handleInitialSubmit(p.prompt), disabled: loading, className: "bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 text-gray-800 dark:text-gray-200" }, p.label))) : /* @__PURE__ */ import_react.default.createElement("div", { className: "mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 rounded-lg text-sm flex items-center gap-2 border border-blue-200 dark:border-blue-800" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Check, { size: 16, className: "shrink-0" }), /* @__PURE__ */ import_react.default.createElement("span", { className: "truncate" }, "Document locked for editing. Use the chat pane to request further changes or variations!"))), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1 flex flex-col p-4 bg-white dark:bg-gray-900 h-[50vh] xl:h-full relative overflow-hidden" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex justify-between items-center mb-4" }, /* @__PURE__ */ import_react.default.createElement("h2", { className: "font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2" }, /* @__PURE__ */ import_react.default.createElement(MessageSquare, { size: 18 }), "Corrections & Chat"), /* @__PURE__ */ import_react.default.createElement(
      "button",
      {
        onClick: () => setShowConfig(!showConfig),
        className: "flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      },
      /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Settings, { size: 16 }),
      "Config",
      showConfig ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.ChevronUp, { size: 16 }) : /* @__PURE__ */ import_react.default.createElement(import_lucide_react.ChevronDown, { size: 16 })
    )), showConfig && /* @__PURE__ */ import_react.default.createElement("div", { className: "mb-4 bg-gray-50 dark:bg-gray-800 p-4 rounded-xl border dark:border-gray-700 shadow-sm flex flex-col gap-3 transition-all text-sm shrink-0" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex flex-col md:flex-row gap-4" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Model"), /* @__PURE__ */ import_react.default.createElement("select", { value: config.model, onChange: (e) => updateConfigAPI("model", e.target.value), className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-gray-900 dark:text-gray-100" }, /* @__PURE__ */ import_react.default.createElement("option", { value: "~deepseek/deepseek-v4-flash-latest" }, "v4-flash"), models.map((m) => /* @__PURE__ */ import_react.default.createElement("option", { key: m.id, value: m.id }, m.id)))), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Thinking Effort"), /* @__PURE__ */ import_react.default.createElement("select", { value: config.thinking, onChange: (e) => updateConfigAPI("thinking", e.target.value), className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-gray-900 dark:text-gray-100" }, /* @__PURE__ */ import_react.default.createElement("option", { value: "none" }, "None"), /* @__PURE__ */ import_react.default.createElement("option", { value: "enabled" }, "Enabled"))), /* @__PURE__ */ import_react.default.createElement("div", { className: "w-20" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500 mb-1" }, "Mem"), /* @__PURE__ */ import_react.default.createElement("input", { type: "number", value: config.memory_limit, onChange: (e) => updateConfigAPI("memory_limit", parseInt(e.target.value) || 20), className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-1.5 text-gray-900 dark:text-gray-100" }))), /* @__PURE__ */ import_react.default.createElement("div", null, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex justify-between items-center mb-1" }, /* @__PURE__ */ import_react.default.createElement("label", { className: "block text-xs font-medium text-gray-500" }, "System Prompt"), /* @__PURE__ */ import_react.default.createElement(
      "button",
      {
        onClick: (e) => {
          e.preventDefault();
          updateConfigAPI("system_prompt", settings.CORRECTION_PROMPT || "");
        },
        className: "text-[10px] px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded text-gray-600 dark:text-gray-300 transition-colors",
        title: "Restore to Default"
      },
      "Restore Default"
    )), /* @__PURE__ */ import_react.default.createElement("textarea", { value: config.system_prompt, onChange: (e) => updateConfigAPI("system_prompt", e.target.value), rows: "3", className: "w-full border dark:border-gray-600 dark:bg-gray-700 rounded p-2 font-mono focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-gray-100" }))), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex-1 overflow-y-auto mb-4 bg-gray-50 dark:bg-gray-950 rounded-xl border dark:border-gray-800 shadow-inner p-4 space-y-6" }, correctionChats.length === 0 && !loading && /* @__PURE__ */ import_react.default.createElement("div", { className: "h-full flex flex-col items-center justify-center text-gray-400 gap-2" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Wand2, { size: 32, className: "opacity-20" }), /* @__PURE__ */ import_react.default.createElement("p", null, "No corrections yet. Paste text on the left and submit!")), correctionChats.map((c, i) => /* @__PURE__ */ import_react.default.createElement("div", { key: c.id || i, className: `flex flex-col ${c.role === "user" ? "items-end" : "items-start"}` }, /* @__PURE__ */ import_react.default.createElement("div", { className: `max-w-[90%] md:max-w-[85%] rounded-xl overflow-hidden shadow-sm ${c.role === "user" ? "bg-blue-600 text-white" : "bg-white dark:bg-gray-800 border dark:border-gray-700"}` }, /* @__PURE__ */ import_react.default.createElement("div", { className: `flex justify-between items-center px-3 py-1.5 border-b ${c.role === "user" ? "bg-blue-700 border-blue-500" : "bg-gray-100 dark:bg-gray-900 border-gray-200 dark:border-gray-700"}` }, /* @__PURE__ */ import_react.default.createElement("span", { className: "font-bold text-xs opacity-80" }, c.role === "user" ? "You" : "AI"), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex gap-1" }, c.role === "user" && /* @__PURE__ */ import_react.default.createElement(import_react.default.Fragment, null, /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => {
      setEditingChatId(c.id);
      setEditingContent(c.content);
    }, className: "p-1 hover:bg-white/20 rounded" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Pencil, { size: 12 })), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => handleDeleteChat(c.id), className: "p-1 hover:bg-white/20 rounded" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Trash2, { size: 12 }))), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => {
      navigator.clipboard.writeText(c.content);
      alert("Copied!");
    }, className: "p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Copy, { size: 12 })))), /* @__PURE__ */ import_react.default.createElement("div", { className: "p-4 prose prose-sm dark:prose-invert max-w-none break-words" }, editingChatId === c.id ? /* @__PURE__ */ import_react.default.createElement("div", { className: "flex flex-col gap-2" }, /* @__PURE__ */ import_react.default.createElement("textarea", { value: editingContent, onChange: (e) => setEditingContent(e.target.value), className: "w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 border rounded p-2 focus:outline-none", rows: "4" }), /* @__PURE__ */ import_react.default.createElement("div", { className: "flex justify-end gap-2" }, /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => setEditingChatId(null), className: "p-1.5 bg-gray-200 dark:bg-gray-700 rounded" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.X, { size: 14 })), /* @__PURE__ */ import_react.default.createElement("button", { onClick: () => handleSaveEdit(c.id), className: "p-1.5 bg-green-500 text-white rounded" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Check, { size: 14 })))) : /* @__PURE__ */ import_react.default.createElement(import_react_markdown.default, { remarkPlugins: [import_remark_gfm.default] }, c.content))))), loading && correctionChats.length > 0 && /* @__PURE__ */ import_react.default.createElement("div", { className: "flex items-start" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "bg-white dark:bg-gray-800 border dark:border-gray-700 p-4 rounded-xl rounded-tl-none shadow-sm" }, /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin text-blue-500", size: 20 }))), /* @__PURE__ */ import_react.default.createElement("div", { ref: chatEndRef })), currentCorrection && !currentCorrection.isTemp && /* @__PURE__ */ import_react.default.createElement("div", { className: "shrink-0 flex flex-col gap-2" }, /* @__PURE__ */ import_react.default.createElement("div", { className: "flex gap-2 overflow-x-auto pb-2 scrollbar-hide" }, PRESETS.map((p) => /* @__PURE__ */ import_react.default.createElement("button", { key: p.label, onClick: (e) => handleChatSubmit(e, p.prompt), disabled: loading, className: "shrink-0 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-800 dark:text-gray-200 text-xs px-3 py-1.5 rounded-full font-medium transition-colors disabled:opacity-50 whitespace-nowrap" }, "Make it ", p.label))), /* @__PURE__ */ import_react.default.createElement("form", { onSubmit: handleChatSubmit, className: "flex gap-2" }, /* @__PURE__ */ import_react.default.createElement(
      "input",
      {
        type: "text",
        value: chatInput,
        onChange: (e) => setChatInput(e.target.value),
        placeholder: "Ask AI to adjust the text further...",
        className: "flex-1 border dark:border-gray-600 dark:bg-gray-800 rounded-lg p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-gray-100",
        disabled: loading
      }
    ), /* @__PURE__ */ import_react.default.createElement("button", { disabled: loading || !chatInput.trim(), type: "submit", className: "bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition-colors disabled:opacity-50 flex items-center justify-center" }, loading ? /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Loader2, { className: "animate-spin", size: 20 }) : /* @__PURE__ */ import_react.default.createElement(import_lucide_react.Send, { size: 20 }))))));
  }

  // ../test_render.jsx
  var props = {
    tabId: "init",
    fetchCorrections: () => {
    },
    settings: {},
    models: [],
    onUpdateTab: () => {
    },
    initialCorrection: null
  };
  try {
    console.log((0, import_server.renderToString)(/* @__PURE__ */ import_react2.default.createElement(CorrectionTab, { ...props })));
    console.log("RENDER SUCCESSFUL");
  } catch (e) {
    console.error("RENDER FAILED:", e);
  }
})();
