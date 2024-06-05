let hash;

function load() {
  document.getElementById("new").setAttribute("hidden", "");

  fetch("/api/admin")
    .then((response) => (response.json()))
    .then((json) => {
      if (json.any) {
        let output;
        hash = json.post_info.hash;

        if (json.post_info.ext === ".mp4") {
          output = `<p><video class="focus" controls src="${url}/${json.post_info.hash}${json.post_info.ext}"></video></p>`;
        } else {
          output = `<p><img class="focus" src="${url}/${json.post_info.hash}${json.post_info.ext}"></p>`;
        }

        output += "<button onclick='save();'>Save</button> <button onclick='remove();'>Delete</button>"

        for (const tag of json.tags) {
          output += `<p><input type="checkbox" id="checkbox-${tag.tag}"> <a href="javascript:(()=>{addTag('${tag.tag}')})()">(${tag.count}) ${tag.tag}</a></p>`;
        }

        document.getElementById("post").innerHTML = output;
        document.getElementById("new").removeAttribute("hidden");
      } else {
        document.getElementById("post").innerText = "All clear! No pending reviews.";
      }
    })
    .catch((err) => {
      document.getElementById("post").innerHTML = `Something went wrong loading! (${err})<p><button onclick='load();'>Retry...</button></p>`
    });
}

function addTag(tag) {
  let x = document.getElementById(`checkbox-${tag}`);
  x.checked = !x.checked;
}

function save() {
  let tags = [];

  for (const input of document.querySelectorAll("input")) {
    if (input.checked) {
      tags.push(input.id.replace("checkbox-", ""));
    }
  }

  fetch("/api/admin", {
    "method": "POST",
    "body": JSON.stringify({
      hash: hash,
      tags: tags
    })
  });
}

function remove() {
  fetch("/api/admin", {
    "method": "DELETE",
    "body": JSON.stringify({
      hash: hash
    })
  }).then((response) => (response.json()))
    .then((json) => {
      if (json.success) {
        load();
      } else {
        throw json
      }
    })
    .catch((err) => {
      alert(err);
    });
}

const url = document.getElementById("url").innerText;
document.getElementById("url").remove();

load();
