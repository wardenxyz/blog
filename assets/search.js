/**
 * Blog search functionality
 */

// Store the loaded search index
let searchIndex = null;

// DOM elements
const searchInput = document.getElementById("search-input");
const searchResultsContainer = document.getElementById("search-results");
const loadingIndicator = document.getElementById("loading-indicator");

// Keyboard navigation variables
let selectedResultIndex = -1;
let searchResults = [];

/**
 * Initialize the search functionality
 */
function initSearch() {
	// Load the search index when the page loads
	loadSearchIndex();

	// Add event listener for the search input
	searchInput.addEventListener("input", debounce(performSearch, 300));

	// Add keyboard navigation event listeners
	document.addEventListener("keydown", handleKeyboardNavigation);
}

/**
 * Load the search index JSON file
 */
async function loadSearchIndex() {
	if (searchIndex !== null) {
		return; // Already loaded
	}

	try {
		showLoading(true);
		const response = await fetch("/search-index.json");
		if (!response.ok) {
			throw new Error("Failed to load search index");
		}

		searchIndex = await response.json();
		showLoading(false);
	} catch (error) {
		console.error("Error loading search index:", error);
		showError("Failed to load search data. Please try refreshing the page.");
		showLoading(false);
	}
}

/**
 * Perform search based on the current input value
 */
function performSearch() {
	const query = searchInput.value.trim().toLowerCase();

	if (!searchIndex) {
		showMessage("Search index is still loading. Please try again in a moment.");
		return;
	}

	if (query.length < 2) {
		searchResultsContainer.innerHTML = "";
		selectedResultIndex = -1;
		searchResults = [];
		return;
	}

	searchResults = searchIndex.filter((post) => {
		// Search in title, content, tags, category
		return (
			post.title.toLowerCase().includes(query) ||
			post.content.toLowerCase().includes(query) ||
			(post.tags &&
				post.tags.some((tag) => tag.toLowerCase().includes(query))) ||
			(post.category &&
				((typeof post.category === "string" &&
					post.category.toLowerCase().includes(query)) ||
					(Array.isArray(post.category) &&
						post.category.some((cat) => cat.toLowerCase().includes(query)))))
		);
	});

	displayResults(searchResults, query);
	// Reset selected item when search results change
	selectedResultIndex = -1;
}

/**
 * Display search results
 */
function displayResults(results, query) {
	if (results.length === 0) {
		searchResultsContainer.innerHTML = `
            <div class="search-no-results">
                No results found for "${escapeHtml(query)}".
            </div>
        `;
		return;
	}

	let html = "";

	results.forEach((post, index) => {
		// Create snippet by finding context around the matched term
		let snippet = createSnippet(post.content, query);

		// Highlight the search term in title and snippet
		const highlightedTitle = highlightText(post.title, query);
		const highlightedSnippet = highlightText(snippet, query);

		// Format date if available
		let dateHtml = "";
		if (post.date && post.date !== "Unknown date") {
			dateHtml = `<span class="date">${post.date}</span>`;
		}

		// Format tags if available
		let tagsHtml = "";
		if (post.tags && post.tags.length > 0) {
			tagsHtml = `<span class="tags">Tags: ${post.tags
				.map((tag) => `<a href="/tags.html#${tag}">${tag}</a>`)
				.join(", ")}</span>`;
		}

		// Format category if available
		let categoryHtml = "";
		if (post.category) {
			if (typeof post.category === "string") {
				categoryHtml = `<span class="category">Category: <a href="/categories.html#${post.category}">${post.category}</a></span>`;
			} else if (Array.isArray(post.category) && post.category.length > 0) {
				categoryHtml = `<span class="category">Categories: ${post.category
					.map((cat) => `<a href="/categories.html#${cat}">${cat}</a>`)
					.join(", ")}</span>`;
			}
		}

		// Add search query parameter to post URL
		const postUrl =
			post.url +
			(post.url.includes("?") ? "&" : "?") +
			"highlight=" +
			encodeURIComponent(query);

		html += `
            <div class="search-result-item" data-index="${index}" tabindex="-1">
                <div class="search-result-title">
                    <a href="${postUrl}">${highlightedTitle}</a>
                </div>
                <div class="search-result-meta">
                    ${dateHtml}
                    ${categoryHtml}
                    ${tagsHtml}
                </div>
                <div class="search-result-snippet">${highlightedSnippet}</div>
            </div>
        `;
	});

	searchResultsContainer.innerHTML = html;

	// Add click event listeners to the search results
	addResultClickHandlers();
}

/**
 * Add click event handlers to search result items
 */
function addResultClickHandlers() {
	const resultItems = document.querySelectorAll(".search-result-item");

	resultItems.forEach((item) => {
		// Add click handler to select an item
		item.addEventListener("mouseover", () => {
			clearSelectedResult();
			selectedResultIndex = parseInt(item.getAttribute("data-index"));
			highlightSelectedResult();
		});

		// Add click handler to navigate to the result
		item.addEventListener("click", (e) => {
			// Don't navigate if they clicked on a link inside the item (like tag links)
			if (e.target.tagName.toLowerCase() !== "a") {
				const index = parseInt(item.getAttribute("data-index"));
				if (index >= 0 && index < searchResults.length) {
					// Add search query parameter to URL
					const query = searchInput.value.trim().toLowerCase();
					const url = searchResults[index].url;
					window.location.href =
						url +
						(url.includes("?") ? "&" : "?") +
						"highlight=" +
						encodeURIComponent(query);
				}
			}
		});
	});
}

/**
 * Create a text snippet with context around the search term
 */
function createSnippet(content, query, maxLength = 200) {
	// Strip HTML tags
	const plainText = content.replace(/<[^>]+>/g, " ");

	// Find the index of the search term
	const index = plainText.toLowerCase().indexOf(query.toLowerCase());

	if (index === -1) {
		// If not found, just return the beginning of the content
		return plainText.substring(0, maxLength) + "...";
	}

	// Calculate snippet start and end positions to show context around the match
	let start = Math.max(0, index - maxLength / 2);
	let end = Math.min(plainText.length, index + query.length + maxLength / 2);

	// Adjust to not cut words
	if (start > 0) {
		// Find the next space after our calculated start
		const nextSpace = plainText.indexOf(" ", start);
		if (nextSpace !== -1 && nextSpace < index) {
			start = nextSpace + 1;
		}
	}

	if (end < plainText.length) {
		// Find the previous space before our calculated end
		const prevSpace = plainText.lastIndexOf(" ", end);
		if (prevSpace !== -1 && prevSpace > index + query.length) {
			end = prevSpace;
		}
	}

	// Create snippet
	let snippet = plainText.substring(start, end);

	// Add ellipsis if needed
	if (start > 0) snippet = "..." + snippet;
	if (end < plainText.length) snippet += "...";

	return snippet;
}

/**
 * Highlight the search term in text
 */
function highlightText(text, query) {
	if (!query) return text;

	const regex = new RegExp(`(${escapeRegExp(query)})`, "gi");
	return text.replace(regex, '<span class="search-highlight">$1</span>');
}

/**
 * Show or hide loading indicator
 */
function showLoading(isLoading) {
	if (loadingIndicator) {
		loadingIndicator.style.display = isLoading ? "block" : "none";
	}
}

/**
 * Display an error message
 */
function showError(message) {
	searchResultsContainer.innerHTML = `
        <div class="search-no-results">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

/**
 * Display a message
 */
function showMessage(message) {
	searchResultsContainer.innerHTML = `
        <div class="search-no-results">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
	return text
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/"/g, "&quot;")
		.replace(/'/g, "&#039;");
}

/**
 * Escape regexp special characters
 */
function escapeRegExp(string) {
	return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Debounce function to limit the rate at which a function can fire
 */
function debounce(func, wait) {
	let timeout;
	return function () {
		const context = this;
		const args = arguments;
		const later = function () {
			timeout = null;
			func.apply(context, args);
		};
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
	};
}

// Function to focus the search input
function focusSearchInput() {
	if (searchInput) {
		searchInput.focus();
	}
}

/**
 * Handle keyboard navigation for search results
 */
function handleKeyboardNavigation(event) {
	// Only process keyboard navigation when there are search results
	if (searchResults.length === 0) return;

	// Handle arrow keys regardless of focus
	switch (event.key) {
		case "ArrowDown":
			event.preventDefault();
			// If no result is currently selected, select the first one
			if (selectedResultIndex === -1) {
				selectedResultIndex = 0;
				highlightSelectedResult();
				if (document.activeElement === searchInput) {
					searchInput.blur();
				}
			} else {
				selectNextResult();
			}
			break;
		case "ArrowUp":
			event.preventDefault();
			// If no result is currently selected, select the last one
			if (selectedResultIndex === -1) {
				selectedResultIndex = searchResults.length - 1;
				highlightSelectedResult();
				if (document.activeElement === searchInput) {
					searchInput.blur();
				}
			} else {
				selectPreviousResult();
			}
			break;
		case "Enter":
			// Only prevent default and navigate if a result is selected and we're not focused on the search input
			// or the search input is empty
			if (
				selectedResultIndex >= 0 &&
				(document.activeElement !== searchInput ||
					searchInput.value.trim() === "")
			) {
				event.preventDefault();
				navigateToSelectedResult();
			}
			break;
		case "Escape":
			// Clear selection and return focus to search input
			clearSelectedResult();
			selectedResultIndex = -1;
			focusSearchInput();
			break;
	}
}

/**
 * Select the next search result
 */
function selectNextResult() {
	if (searchResults.length === 0) return;

	// Clear current selection
	clearSelectedResult();

	// Move to next result or back to first if at end
	selectedResultIndex = (selectedResultIndex + 1) % searchResults.length;

	// Apply selected styling
	highlightSelectedResult();

	// Blur search input if it's focused to improve keyboard navigation
	if (document.activeElement === searchInput) {
		searchInput.blur();
	}
}

/**
 * Select the previous search result
 */
function selectPreviousResult() {
	if (searchResults.length === 0) return;

	// Clear current selection
	clearSelectedResult();

	// Move to previous result or to last if at beginning
	selectedResultIndex =
		selectedResultIndex <= 0
			? searchResults.length - 1
			: selectedResultIndex - 1;

	// Apply selected styling
	highlightSelectedResult();

	// Blur search input if it's focused to improve keyboard navigation
	if (document.activeElement === searchInput) {
		searchInput.blur();
	}
}

/**
 * Navigate to the currently selected search result
 */
function navigateToSelectedResult() {
	if (selectedResultIndex >= 0 && selectedResultIndex < searchResults.length) {
		const url = searchResults[selectedResultIndex].url;
		if (url) {
			// Add search query parameter to URL
			const query = searchInput.value.trim().toLowerCase();
			window.location.href =
				url +
				(url.includes("?") ? "&" : "?") +
				"highlight=" +
				encodeURIComponent(query);
		}
	}
}

/**
 * Clear styling from the current selected result
 */
function clearSelectedResult() {
	const selectedItems = document.querySelectorAll(
		".search-result-item-selected",
	);
	selectedItems.forEach((item) => {
		item.classList.remove("search-result-item-selected");
	});
}

/**
 * Highlight the currently selected result
 */
function highlightSelectedResult() {
	if (selectedResultIndex >= 0) {
		const selectedItem = document.querySelector(
			`.search-result-item[data-index="${selectedResultIndex}"]`,
		);
		if (selectedItem) {
			selectedItem.classList.add("search-result-item-selected");
			selectedItem.scrollIntoView({ behavior: "smooth", block: "nearest" });
		}
	}
}

// Initialize search when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
	initSearch();

	// If we're on the search page and came from a click on the search nav link,
	// focus the search input automatically
	if (document.referrer && document.referrer.includes(window.location.origin)) {
		focusSearchInput();
	}

	// Check for URL parameter that indicates we should focus
	const urlParams = new URLSearchParams(window.location.search);
	if (urlParams.has("focus") && urlParams.get("focus") === "true") {
		focusSearchInput();
	}
});
