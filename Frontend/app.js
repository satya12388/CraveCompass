const API_URL = "https://cravecompass-api.onrender.com/analyze";

const uploadBtn = document.getElementById("upload-btn");
const imageUpload = document.getElementById("image-upload");
const fileName = document.getElementById("file-name");
const queryInput = document.getElementById("query-input");
const analyzeBtn = document.getElementById("analyze-btn");
const errorMessage = document.getElementById("error-message");

const inputSection = document.getElementById("input-section");
const outputSection = document.getElementById("output-section");
const loadingDiv = document.getElementById("loading");
const resultsContainer = document.getElementById("results-container");
const backBtn = document.getElementById("back-btn");

let selectedFile = null;

// Handle file selection
const uploadArea = document.querySelector(".upload-area");
const fileIndicator = document.getElementById("file-indicator");

uploadArea.addEventListener("click", () => {
  imageUpload.click();
});

imageUpload.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    selectedFile = e.target.files[0];
    fileName.textContent = selectedFile.name;
    uploadArea.classList.add("hidden");
    fileIndicator.classList.remove("hidden");
    analyzeBtn.disabled = false;
  }
});

function showError(msg) {
  errorMessage.textContent = msg;
  errorMessage.classList.remove("hidden");
}

function hideError() {
  errorMessage.classList.add("hidden");
}

// Handle Analyze button
analyzeBtn.addEventListener("click", async () => {
  hideError();

  if (!selectedFile) {
    showError("Please upload a menu image first.");
    return;
  }

  if (!queryInput.value.trim()) {
    showError("Please enter what you are craving.");
    return;
  }

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("query", queryInput.value.trim());

  // Show loading UI
  analyzeBtn.disabled = true;
  loadingDiv.classList.remove("hidden");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      let errorMsg = data.detail || `Server error: ${response.status}`;
      // Catch long messy Pydantic validation logs and show a clean message
      if (
        errorMsg.includes("validation error") ||
        errorMsg.includes("Failed to parse")
      ) {
        errorMsg =
          "The AI couldn't confidently read the items on this menu. Please try a clearer or simpler image!";
      }
      throw new Error(errorMsg);
    }

    if (data.success && data.data) {
      // Ensure data.data is an array (even if it's a single object)
      const items = Array.isArray(data.data) ? data.data : [data.data];

      if (items.length > 0) {
        renderResults(items);
        inputSection.classList.remove("active");
        outputSection.classList.add("active");
      } else {
        throw new Error("No recommendations found.");
      }
    } else {
      throw new Error("Invalid response format from server.");
    }
  } catch (err) {
    showError(err.message || "Failed to connect to the server.");
  } finally {
    // Hide loading UI
    analyzeBtn.disabled = false;
    loadingDiv.classList.add("hidden");
  }
});

// Render Results DOM
function renderResults(items) {
  resultsContainer.innerHTML = "";

  items.forEach((item) => {
    const itemDiv = document.createElement("div");
    itemDiv.className = "result-item";

    // Choose category badge styling
    const category = item.category || "Unknown";
    let categoryClass = "veg-badge";
    if (category.toLowerCase() === "non-veg") categoryClass = "non-veg-badge";
    else if (category.toLowerCase() === "beverages")
      categoryClass = "bev-badge";
    else if (category.toLowerCase() === "desserts") categoryClass = "des-badge";
    else if (category.toLowerCase() !== "veg") categoryClass = "other-badge";

    const categoryBadgeHtml =
      category !== "Unknown"
        ? `<div class="category-badge ${categoryClass}">${category}</div>`
        : "";

    itemDiv.innerHTML = `
        <div class="result-title-row">
            <div class="title-group">
                <div>
                  <div class="result-name">${item.name}</div>
                  ${categoryBadgeHtml}
                </div>
            </div>
            <div class="result-price">${item.price}</div>
        </div>
        
        <button class="btn outline-btn mt-3 fetch-details-btn" onclick="fetchItemDetails('${item.name.replace(/'/g, "\\'")}', this)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
            View Recipe Insights
        </button>
    `;

    resultsContainer.appendChild(itemDiv);
  });
}

// --- Modal Logic ---
const itemModal = document.getElementById("item-modal");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const closeModalBtn = document.getElementById("close-modal-btn");

function closeModal() {
  if (itemModal) itemModal.classList.add("hidden");
  if (modalBody) modalBody.innerHTML = "";
}

if (closeModalBtn) {
  closeModalBtn.addEventListener("click", closeModal);
}
if (itemModal) {
  itemModal.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-backdrop")) {
      closeModal();
    }
  });
}

// Fetch detailed insights from the new LLM Search Agent
async function fetchItemDetails(itemName, btnElement) {
  const originalBtnText = btnElement.innerHTML;

  // Set Button Loading State
  btnElement.disabled = true;
  btnElement.innerHTML = `<div class="spinner-small"></div>`;

  // Show Modal Loading State
  modalTitle.textContent = itemName;
  modalBody.innerHTML = `
    <div style="text-align:center; padding: 2rem;">
        <div class="spinner" style="margin: 0 auto; border-top-color: var(--primary);"></div>
        <p style="color: var(--text-muted); margin-top: 1rem;">Consulting Culinary AI...</p>
    </div>
  `;
  itemModal.classList.remove("hidden");

  try {
    const response = await fetch(
      `https://cravecompass-api.onrender.com/item-details?item_name=${encodeURIComponent(itemName)}`,
    );

    if (!response.ok) {
      throw new Error("Failed to fetch details");
    }

    const data = await response.json();

    let nutritionTags = "";
    if (
      data.nutritioninfo &&
      typeof data.nutritioninfo === "object" &&
      !Array.isArray(data.nutritioninfo)
    ) {
      const info = data.nutritioninfo;
      const tags = [];
      if (info.calories)
        tags.push(
          `<span class="tag tag-nutrition">Calories: ${info.calories}</span>`,
        );
      if (info.protein)
        tags.push(
          `<span class="tag tag-nutrition">Protein: ${info.protein}</span>`,
        );
      if (info.carbs)
        tags.push(
          `<span class="tag tag-nutrition">Carbs: ${info.carbs}</span>`,
        );
      if (info.fat)
        tags.push(`<span class="tag tag-nutrition">Fat: ${info.fat}</span>`);
      nutritionTags = tags.join("");
    } else if (Array.isArray(data.nutritioninfo)) {
      // Fallback for older format just in case
      nutritionTags = data.nutritioninfo
        .map((n) => `<span class="tag tag-nutrition">${n}</span>`)
        .join("");
    }
    const ingredientTags = (data.ingredients || [])
      .map((i) => `<span class="tag tag-ingredient">${i}</span>`)
      .join("");

    let safePrep = "N/A";
    if (Array.isArray(data.preparation) && data.preparation.length > 0) {
      safePrep =
        `<ul class="prep-list" style="margin: 0; padding-left: 1rem;">` +
        data.preparation
          .map((step) => `<li style="margin-bottom: 0.25rem;">${step}</li>`)
          .join("") +
        `</ul>`;
    } else if (
      typeof data.preparation === "string" &&
      data.preparation.trim() !== ""
    ) {
      safePrep = data.preparation;
    }

    let imageHtml = "";
    if (data.image_url) {
      imageHtml = `<div class="detail-image" style="background-image: url('${data.image_url}');"></div>`;
    }

    modalBody.innerHTML = `
          ${imageHtml}
          <div class="result-detail">
              <strong><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"></path><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg> Chef's Preparation</strong>
              <div style="margin-top: 0.5rem; line-height: 1.5;">${safePrep}</div>
          </div>
          
          <div class="result-detail mt-3">
              <strong><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="14.31" y1="8" x2="20.05" y2="17.94"></line><line x1="9.69" y1="8" x2="21.17" y2="8"></line><line x1="7.38" y1="12" x2="13.12" y2="2.06"></line><line x1="9.69" y1="16" x2="3.95" y2="6.06"></line><line x1="14.31" y1="16" x2="2.83" y2="16"></line><line x1="16.62" y1="12" x2="10.88" y2="21.94"></line></svg> Authentic Ingredients</strong>
              <div class="tags-container">${ingredientTags || '<span class="tag tag-ingredient">N/A</span>'}</div>
          </div>
          
          <div class="result-detail mt-3">
              <strong><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg> Nutritional Profile</strong>
              <div class="tags-container">${nutritionTags || '<span class="tag tag-nutrition">N/A</span>'}</div>
          </div>
      `;

    btnElement.innerHTML = originalBtnText; // Restore Original View Details Button
    btnElement.disabled = false;
  } catch (err) {
    modalBody.innerHTML = `<div class="error" style="margin-top:0; padding:1rem;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg> Failed to load details.</div>`;
    btnElement.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg> Retry Insights`;
    btnElement.disabled = false;
  }
}

const clearFileBtn = document.getElementById("clear-file-btn");

// Handle clear file
clearFileBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  selectedFile = null;
  imageUpload.value = "";
  fileIndicator.classList.add("hidden");
  uploadArea.classList.remove("hidden");
  analyzeBtn.disabled = true;
  hideError();
});

// Handle Back Button
backBtn.addEventListener("click", () => {
  outputSection.classList.remove("active");
  inputSection.classList.add("active");
  // Keep the uploaded image! Do not clear state.
});
