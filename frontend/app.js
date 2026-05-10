const API_BASE_URL = "http://localhost:8000";

const form = document.querySelector("#chatForm");
const questionInput = document.querySelector("#question");
const sendButton = document.querySelector("#sendButton");
const sampleButton = document.querySelector("#sampleButton");
const reportSampleButton = document.querySelector("#reportSampleButton");
const alertBox = document.querySelector("#alert");
const chatMessages = document.querySelector("#chatMessages");
const resultPanel = document.querySelector("#result");
const sqlOutput = document.querySelector("#sqlOutput");
const downloadLink = document.querySelector("#downloadLink");
const connectionState = document.querySelector("#connectionState");

sampleButton.addEventListener("click", () => {
  questionInput.value = "What tables and columns are available?";
  questionInput.focus();
});

reportSampleButton.addEventListener("click", () => {
  questionInput.value = "Generate a PDF report showing total revenue by region";
  questionInput.focus();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) {
    showError("Enter a message first.");
    return;
  }

  setLoading(true);
  hideError();
  resultPanel.classList.add("hidden");
  addMessage("user", question);
  questionInput.value = "";

  try {
    const response = await fetch(`${API_BASE_URL}/generate-report`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || "Request failed. Check backend logs for details.");
    }

    addMessage("assistant", data.answer || "Done.");

    if (data.mode === "report") {
      sqlOutput.textContent = data.sql_query || "No SQL returned.";
      downloadLink.href = `${API_BASE_URL}/reports/${encodeURIComponent(data.pdf_path || "report.pdf")}`;
      resultPanel.classList.remove("hidden");
    }

    connectionState.textContent = "Complete";
  } catch (error) {
    showError(error.message);
    addMessage("assistant error-message", error.message);
    connectionState.textContent = "Needs attention";
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  sendButton.innerHTML = isLoading
    ? '<span class="button-icon">...</span> Thinking'
    : '<span class="button-icon">></span> Send';
  connectionState.textContent = isLoading ? "Working" : connectionState.textContent;
}

function addMessage(role, text) {
  const message = document.createElement("article");
  message.className = `message ${role}`;
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  message.appendChild(paragraph);
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showError(message) {
  alertBox.textContent = message;
  alertBox.classList.remove("hidden");
}

function hideError() {
  alertBox.textContent = "";
  alertBox.classList.add("hidden");
}
