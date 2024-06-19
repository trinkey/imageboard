const maxSuggestions = 10;

function getSuggestions(query) {
  if (!query) {
    return [];
  }

  let suggestions = [];

  for (const tag of tags) {
    if (tag.tag.indexOf(query) == 0) {
      suggestions.push(tag);

      if (suggestions.length >= maxSuggestions) {
        return suggestions;
      }
    }
  }

  for (const tag of tags) {
    if (tag.tag.indexOf(query) > 0) {
      suggestions.push(tag);

      if (suggestions.length >= maxSuggestions) {
        return suggestions.sort((a, b) => (a.count < b.count));
      }
    }
  }

  return suggestions.sort((a, b) => (a.count < b.count));
}

function completeSuggestion(tag) {
  let input = document.getElementById("search");
  let str = input.value;
  str = str.split(" ").slice(0, str.split(" ").length - 1).join(" ")

  input.value = `${str}${str ? " " : ""}${tag} `;
  input.focus();
  setSuggestions();
}

function setSuggestions() {
  let input = document.getElementById("search")

  let suggestions = getSuggestions(input.value.split(" ")[input.value.split(" ").length - 1]);
  let html = "";

  for (const suggestion of suggestions) {
    html += `<div class="search-suggestion" onclick="completeSuggestion('${escapeHTML(suggestion.tag)}');">(${suggestion.count}) ${escapeHTML(suggestion.tag)}</div>`;
  }

  document.getElementById("search-after").innerHTML = html;
}

let escapeHTML = (str) => (str.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll("\"", "&quo;").replaceAll("'", "&squo;"));

if (document.getElementById("search-after") && document.getElementById("search")) {
  document.getElementById("search").addEventListener("input", setSuggestions);
}
