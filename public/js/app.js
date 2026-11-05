(() => {
  const rows = document.getElementById("grocery-rows");
  const empty = document.getElementById("empty-state");
  const count = document.getElementById("item-count");
  const progress = document.getElementById("progress-text");
  const form = document.getElementById("add-form");
  const itemInput = document.getElementById("item-input");
  const quantityInput = document.getElementById("quantity-input");
  const toast = document.getElementById("toast");

  function notify(message) {
    toast.textContent = message;
    toast.classList.add("show");
    window.clearTimeout(notify.timer);
    notify.timer = window.setTimeout(() => toast.classList.remove("show"), 2200);
  }

  function render() {
    const items = window.GroceryList.getAll();
    const purchased = items.filter(item => item.purchased).length;
    count.textContent = items.length;
    progress.textContent = `${purchased} of ${items.length} purchased`;
    empty.hidden = items.length > 0;
    rows.replaceChildren();

    items.forEach(item => {
      const tr = document.createElement("tr");
      if (item.purchased) tr.classList.add("completed-row");

      const checkCell = document.createElement("td");
      const check = document.createElement("input");
      check.type = "checkbox";
      check.className = "row-check";
      check.checked = item.purchased;
      check.setAttribute("aria-label", `Mark ${item.name} as purchased`);
      check.addEventListener("change", () => {
        window.GroceryList.update(item.id, { purchased: check.checked });
        render();
      });
      checkCell.append(check);

      const nameCell = document.createElement("td");
      const name = document.createElement("span");
      name.className = `item-name${item.purchased ? " completed" : ""}`;
      name.textContent = item.name;
      nameCell.append(name);

      const quantityCell = document.createElement("td");
      quantityCell.className = "quantity-cell";
      const quantity = document.createElement("input");
      quantity.value = item.quantity;
      quantity.maxLength = 60;
      quantity.setAttribute("aria-label", `Quantity for ${item.name}`);
      quantity.addEventListener("change", () => {
        window.GroceryList.update(item.id, { quantity: quantity.value });
        notify("Quantity updated");
      });
      quantityCell.append(quantity);

      const actionCell = document.createElement("td");
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "delete-button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove ${item.name}`);
      remove.addEventListener("click", () => {
        window.GroceryList.remove(item.id);
        render();
        notify("Item removed");
      });
      actionCell.append(remove);

      tr.append(checkCell, nameCell, quantityCell, actionCell);
      rows.append(tr);
    });
  }

  form.addEventListener("submit", event => {
    event.preventDefault();
    if (!window.GroceryList.add(itemInput.value, quantityInput.value)) {
      itemInput.focus();
      return;
    }
    itemInput.value = "";
    quantityInput.value = "";
    itemInput.focus();
    render();
    notify("Added to your list");
  });

  document.querySelectorAll("[data-item]").forEach(button => {
    button.addEventListener("click", () => {
      window.GroceryList.add(button.dataset.item, button.dataset.quantity || "");
      render();
      notify(`${button.dataset.item} added`);
    });
  });

  document.getElementById("clear-completed").addEventListener("click", () => {
    window.GroceryList.clearCompleted();
    render();
    notify("Completed items cleared");
  });

  function formatList() {
    const items = window.GroceryList.getAll();
    if (!items.length) return "";
    return ["Grocery List", ...items.map(item =>
      `${item.purchased ? "[x]" : "[ ]"} ${item.name}${item.quantity ? " - " + item.quantity : ""}`
    )].join("\n");
  }

  document.getElementById("copy-list").addEventListener("click", async () => {
    const text = formatList();
    if (!text) return notify("Your list is empty");
    try {
      await navigator.clipboard.writeText(text);
      notify("List copied");
    } catch {
      notify("Clipboard access is unavailable in this browser");
    }
  });

  document.getElementById("share-list").addEventListener("click", async () => {
    const text = formatList();
    if (!text) return notify("Your list is empty");
    if (navigator.share) {
      try { await navigator.share({ title: "Grocery List", text }); }
      catch (error) { if (error.name !== "AbortError") notify("Could not share list"); }
    } else {
      try {
        await navigator.clipboard.writeText(text);
        notify("Sharing isn't supported here. List copied instead.");
      } catch {
        notify("Sharing isn't supported in this browser");
      }
    }
  });

  window.addEventListener("grocery:storage-error", () => notify("Could not save. Check device storage."));
  render();
})();
