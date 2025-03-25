const PR_SCORES_URL = "https://sairammotupalli.github.io/PRISM";

function injectPRScoresTab() {
  const navBar = document.querySelector("ul.UnderlineNav-body");

  if (!navBar) return;
  if (document.querySelector("#pr-scores-tab")) return;

  const li = document.createElement("li");
  li.setAttribute("data-view-component", "true");
  li.className = "d-inline-flex";

  li.innerHTML = `
    <a id="pr-scores-tab"
       href="${PR_SCORES_URL}"
       class="UnderlineNav-item no-wrap js-responsive-underlinenav-item"
       data-tab-item="i3pr-scores-tab"
       data-view-component="true"
       target="_self">
      <svg aria-hidden="true" height="16" width="16" viewBox="0 0 16 16" version="1.1"
           class="octicon octicon-graph UnderlineNav-octicon d-none d-sm-inline">
        <path d="M1 13h14v1H1zM4 10h1v2H4zm3-5h1v7H7zm3 2h1v5h-1z"></path>
      </svg>
      <span data-content="PR Scores">PR Scores</span>
    </a>
  `;

  navBar.appendChild(li);
}

// Use MutationObserver to wait for nav bar to be added
const observer = new MutationObserver(() => {
  injectPRScoresTab();
});

observer.observe(document.body, { childList: true, subtree: true });

// Also run immediately in case it's already loaded
injectPRScoresTab();
