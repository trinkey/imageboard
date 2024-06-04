const urlParams = new URLSearchParams(window.location.search);

if (urlParams.get("reason")) {
  let x = document.createElement("div");
  x.classList.add("error");
  x.id = "status";
  x.innerHTML = "<h2>Uh oh!</h2>";

  switch (urlParams.get("reason")) {
    case ("success"):
      x.classList.add("success");
      x.classList.remove("error");
      x.innerHTML = "<h2>Success!</h2>Your file is now in the review process and should be up within 3-4 business days.";
      break;

    case ("type"):
    case ("invalid"):
      x.innerHTML += "Your file doesn't seem to be a valid png, jpg, gif, or mp4!";
      break;
    case ("size"):
      x.innerHTML += "The file you're trying to upload is too large!";
      break;
    case ("exists"):
      x.innerHTML += "The file you're trying to upload seems to already exist!";
      break;
  }

  x.innerHTML += "<p><a style='color: var(--subtext0);' href='javascript:document.getElementById(&quot;status&quot;).remove();'><small>Dismiss...</small></a></p>"
  document.getElementById("status").replaceWith(x);
}

document.getElementById("file").onchange = function() {
  document.getElementById("content-type").value = this.files[0].type;

  if (this.files[0].size > 1024 * 1024 * 20) { // 20mb
    alert("File is too big!");
    this.value = "";
  }
};
