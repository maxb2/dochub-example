// Stolen from https://sentamal.in/articles/static-site-search-with-lunrjs/


/* Async Function to Start LunrJS */
async function startLunrJSAsync() {
    console.log("search: Starting Lunr...");
  
    let idx, pages;
    let ok = false;
  
    const lunrIndex = "lunr-index.json";
    const lunrSummary = "lunr-summary.json";
  
    /* Load the Pre-Built Index */
    console.log("search: Fetching Index...");
    let response = await fetch(lunrIndex);
    let data = await response.json();
    idx = lunr.Index.load(data);
    console.log("search: Index Loaded!");
  
    /* Load the Page Summaries */
    console.log("search: Fetching Summaries...");
    response = await fetch(lunrSummary);
    data = await response.json();
    pages = data;
    console.log("search: Summaries Loaded!");
  
    /* Lunr is Ready; Return */
    console.log("search: Lunr Is Ready!");
    ok = true;
    let obj = {
      idx: idx,
      pages: pages,
      ok: ok
    };
    return obj;
  }
  
  /* Clear the Search Results element then populate with search results */
  function searchSite(search, query) {
    let template = document.querySelector("#search-item");
    let resultsContainer = document.querySelector("#search-results");
  
    resultsContainer.innerHTML = "";
  
    let allResults = search.idx.search(query);
    if (allResults.length === 0) resultsContainer.innerHTML = "<p>Nothing found; search for something else!</p>";
    else allResults.forEach(function (result) {
      let output = document.importNode(template.content, true);
      let title = output.querySelector("a");
      let breadcrumb = output.querySelector("aside");
      let summary = output.querySelector("p");
      let docRef, typemoji;
  
      /* Find the requisite document summary for the search result */
      for (let i=0; i < search.pages.length; i++) {
        if (search.pages[i].id === result.ref) {
          docRef = search.pages[i];
          break;
        }
      }
  
      title.innerHTML = docRef.title;
      title.setAttribute("href", result.ref);
      // breadcrumb.innerHTML = "Don Geronimo » " + docRef.type.charAt(0).toUpperCase() + docRef.type.slice(1) + " » " + docRef.title;
      breadcrumb.innerHTML = "Home » " + docRef.title;
      summary.innerHTML = docRef.summary;
  
      resultsContainer.appendChild(output);
    });
  }
  
  (async () => {
    /* Initialize Lunr */
    let Search = await startLunrJSAsync();
  
    /* If there is a query in the URL, use that as the search query */
    let query;
    let params = new URLSearchParams(document.location.search.substring(1));
    if (params.get("q")) {
      // document.getElementById("ddg-search-value").value = params.get("q");
      query = params.get("q");
      searchSite(Search, query);
    }
  })();