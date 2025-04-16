/**
 * 高亮搜索内容功能
 *
 * 当从搜索页面跳转到文章页面时，自动高亮搜索的关键词
 */

document.addEventListener("DOMContentLoaded", function () {
	// 获取URL中的highlight参数
	const urlParams = new URLSearchParams(window.location.search);
	const highlightQuery = urlParams.get("highlight");

	// 如果存在highlight参数，执行高亮处理
	if (highlightQuery) {
		// 延迟一下执行，确保页面内容都已加载（特别是如果有MathJax等需要渲染的内容）
		setTimeout(() => {
			highlightContentInPage(highlightQuery);
		}, 500);
	}
});

/**
 * 对页面中的内容进行高亮处理
 */
function highlightContentInPage(query) {
	if (!query || query.trim() === "") return;

	// 需要搜索的区域，这里选择了主内容区域
	const contentArea = document.querySelector(".main-content");
	if (!contentArea) return;

	// 将查询词转义为正则表达式安全的字符串
	const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	const regex = new RegExp(`(${escapedQuery})`, "gi");

	// 高亮处理函数
	function highlightText(node) {
		if (node.nodeType === Node.TEXT_NODE) {
			// 如果是文本节点且包含查询词，则替换为高亮的HTML
			const text = node.nodeValue;
			if (regex.test(text)) {
				// 创建一个临时元素来保存HTML
				const span = document.createElement("span");
				span.innerHTML = text.replace(
					regex,
					'<mark class="search-highlight">$1</mark>',
				);

				// 用创建的节点替换原来的文本节点
				const fragment = document.createDocumentFragment();
				while (span.firstChild) {
					fragment.appendChild(span.firstChild);
				}
				node.parentNode.replaceChild(fragment, node);

				return true; // 表示已处理
			}
			return false; // 没有找到匹配
		} else if (
			node.nodeType === Node.ELEMENT_NODE &&
			!["script", "style", "textarea", "pre", "code", "mark"].includes(
				node.nodeName.toLowerCase(),
			)
		) {
			// 如果是元素节点（除了脚本、样式、代码块等），则递归处理其子节点
			let childNodes = Array.from(node.childNodes);
			let didHighlight = false;

			for (let i = 0; i < childNodes.length; i++) {
				// 因为DOM会变化，需要在每次迭代中重新获取最新的子节点
				const currentNode = node.childNodes[i];
				if (currentNode) {
					const wasHighlighted = highlightText(currentNode);
					didHighlight = didHighlight || wasHighlighted;

					// 如果当前节点被处理了，i需要减1，因为节点被替换了
					if (wasHighlighted) {
						i = Math.max(-1, i - 1);
					}
				}
			}

			return didHighlight;
		}

		return false;
	}

	// 开始处理
	const wasHighlighted = highlightText(contentArea);

	// 如果有内容被高亮，滚动到第一个高亮处
	if (wasHighlighted) {
		const firstHighlight = document.querySelector(".search-highlight");
		if (firstHighlight) {
			// 平滑滚动到第一个高亮处
			setTimeout(() => {
				firstHighlight.scrollIntoView({
					behavior: "smooth",
					block: "center",
				});
			}, 300);

			// 添加闪烁效果，引起注意
			firstHighlight.classList.add("highlight-flash");
		}
	}
}

// 添加"返回搜索结果"按钮
document.addEventListener("DOMContentLoaded", function () {
	const urlParams = new URLSearchParams(window.location.search);
	const highlightQuery = urlParams.get("highlight");

	// 如果是从搜索结果页面跳转来的
	if (highlightQuery) {
		// 创建返回搜索结果按钮
		const backButton = document.createElement("button");
		backButton.id = "back-to-search";
		backButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            返回搜索
        `;

		// 添加点击事件
		backButton.addEventListener("click", function () {
			// 返回上一页
			history.back();
		});

		// 插入到页面
		document.body.appendChild(backButton);
	}
});
