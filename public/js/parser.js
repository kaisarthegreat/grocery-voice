(() => {
  const input = document.getElementById("grocery-text");
  const parseButton = document.getElementById("parse-list");
  const status = document.getElementById("parse-status");
  const results = document.getElementById("parse-results");
  const rows = document.getElementById("parsed-items");
  const addButton = document.getElementById("add-parsed-items");
  const language = document.getElementById("voice-language");

  let parsedItems = [];

  function setStatus(message) { status.textContent = message; }

  function render(items) {
    parsedItems = items.map(item => ({ name: item.name || "", quantity: item.quantity || "" }));
    rows.replaceChildren();
    parsedItems.forEach((item, index) => {
      const row = document.createElement("div");
      row.className = "parsed-row";

      const name = document.createElement("input");
      name.value = item.name;
      name.maxLength = 80;
      name.setAttribute("aria-label", `Item ${index + 1}`);
      name.addEventListener("input", () => { parsedItems[index].name = name.value; });

      const quantity = document.createElement("input");
      quantity.value = item.quantity;
      quantity.maxLength = 60;
      quantity.placeholder = "Quantity (optional)";
      quantity.setAttribute("aria-label", `Quantity for item ${index + 1}`);
      quantity.addEventListener("input", () => { parsedItems[index].quantity = quantity.value; });

      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "delete-button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove parsed item ${index + 1}`);
      remove.addEventListener("click", () => {
        parsedItems.splice(index, 1);
        render(parsedItems);
      });

      row.append(name, quantity, remove);
      rows.append(row);
    });
    results.hidden = parsedItems.length === 0;
  }

  parseButton.addEventListener("click", async () => {
    const text = input.value.trim();
    if (!text) {
      setStatus("Speak or type your grocery list first.");
      input.focus();
      return;
    }

    parseButton.disabled = true;
    setStatus("Understanding your list…");
    try {
      const response = await fetch("/api/grocery/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, language: language.value })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || `Server returned ${response.status}`);
      render(data.items || []);
      setStatus(data.count ? `${data.count} item(s) detected. Review before adding.` : "No items detected. Try separating items with commas or 'and'.");
    } catch (error) {
      setStatus(error.message || "Could not process the list. Please try again.");
    } finally {
      parseButton.disabled = false;
    }
  });

  addButton.addEventListener("click", () => {
    const validItems = parsedItems.filter(item => item.name.trim());
    if (!validItems.length) {
      setStatus("There are no valid items to add.");
      return;
    }
    validItems.forEach(item => window.GroceryList.add(item.name, item.quantity));
    render([]);
    input.value = "";
    setStatus(`${validItems.length} item(s) added to your grocery list.`);
    document.getElementById("item-input").focus();
    window.dispatchEvent(new CustomEvent("grocery:list-updated"));
  });
})();
