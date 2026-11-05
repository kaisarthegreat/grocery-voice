(() => {
  const KEY = "grocery-voice.items.v1";
  window.GroceryStorage = {
    load() {
      try {
        const raw = localStorage.getItem(KEY);
        const parsed = raw ? JSON.parse(raw) : [];
        return Array.isArray(parsed) ? parsed : [];
      } catch (error) {
        console.warn("Could not read saved grocery list:", error);
        return [];
      }
    },
    save(items) {
      try {
        localStorage.setItem(KEY, JSON.stringify(items));
        return true;
      } catch (error) {
        console.error("Could not save grocery list:", error);
        return false;
      }
    }
  };
})();
