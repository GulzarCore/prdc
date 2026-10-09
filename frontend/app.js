const form = document.querySelector("#task-form");
const input = document.querySelector("#task-title");
const list = document.querySelector("#task-list");
const message = document.querySelector("#message");
const health = document.querySelector("#health");

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || body.error || `HTTP ${response.status}`);
  }

  return response.status === 204 ? null : response.json();
}

function renderTask(task) {
  const item = document.createElement("li");
  item.className = task.completed ? "done" : "";

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = task.completed;
  checkbox.setAttribute("aria-label", "Mark task complete");

  checkbox.addEventListener("change", async () => {
    try {
      await api(`/api/tasks/${task.id}`, {
        method: "PATCH",
        body: JSON.stringify({ completed: checkbox.checked }),
      });
      await loadTasks();
    } catch (error) {
      message.textContent = error.message;
      checkbox.checked = task.completed;
    }
  });

  const title = document.createElement("span");
  title.textContent = task.title;

  const remove = document.createElement("button");
  remove.textContent = "Delete";
  remove.addEventListener("click", async () => {
    try {
      await api(`/api/tasks/${task.id}`, { method: "DELETE" });
      await loadTasks();
    } catch (error) {
      message.textContent = error.message;
    }
  });

  item.append(checkbox, title, remove);
  return item;
}

async function loadTasks() {
  const tasks = await api("/api/tasks");
  list.replaceChildren(...tasks.map(renderTask));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";

  try {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title: input.value }),
    });
    input.value = "";
    await loadTasks();
  } catch (error) {
    message.textContent = error.message;
  }
});

async function checkHealth() {
  try {
    await api("/readyz");
    health.textContent = "API and database are ready";
  } catch {
    health.textContent = "API or database is unavailable";
  }
}

async function initialize() {
  try {
    await loadTasks();
    await checkHealth();
  } catch (error) {
    message.textContent = error.message;
    health.textContent = "Unable to connect to the application";
  }
}

initialize();