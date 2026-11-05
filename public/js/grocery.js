(() => {
  let items = window.GroceryStorage.load();

  function makeId() {
    return (window.crypto && crypto.randomUUID)
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }

  function persist() {
    const saved = window.GroceryStorage.save(items);
    if (!saved) window.dispatchEvent(new CustomEvent("grocery:storage-error"));
  }

  function getAll() { return items.map(item => ({ ...item })); }

  function add(name, quantity = "") {
    const cleanName = String(name || "").trim();
    if (!cleanName) return false;
    items.push({ id: makeId(), name: cleanName, quantity: String(quantity || "").trim(), purchased: false });
    persist();
    return true;
  }

  function update(id, changes) {
    const item = items.find(entry => entry.id === id);
    if (!item) return false;
    if (typeof changes.name === "string" && changes.name.trim()) item.name = changes.name.trim();
    if (typeof changes.quantity === "string") item.quantity = changes.quantity.trim();
    if (typeof changes.purchased === "boolean") item.purchased = changes.purchased;
    persist();
    return true;
  }

  function remove(id) {
    const before = items.length;
    items = items.filter(item => item.id !== id);
    if (items.length !== before) persist();
  }

  function clearCompleted() {
    const before = items.length;
    items = items.filter(item => !item.purchased);
    if (items.length !== before) persist();
  }

  window.GroceryList = { getAll, add, update, remove, clearCompleted };
})();
