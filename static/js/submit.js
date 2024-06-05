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
      x.innerHTML += "Your file doesn't seem to be a valid png, jpg, gif, or mp4!";
      break;
  }

  x.innerHTML += "<p><a style='color: var(--subtext0);' href='javascript:document.getElementById(&quot;status&quot;).remove();'><small>Dismiss...</small></a></p>"
  document.getElementById("status").replaceWith(x);
}

document.getElementById("file").onchange = function() {
  const files = this.files;
  let allFilesValid = true;

  if (files.length > 20) {
    alert("You can only upload up to 20 files at once!");
    this.value = "";
    return;
  }

  Array.from(files).forEach(file => {
    if (file.size > 1024 * 1024 * 20) { // 20mb
      alert(`File ${file.name} is too big!`);
      allFilesValid = false;
      this.value = "";
      return;
    }
  });

  if (allFilesValid) {
    document.getElementById("content-type").value = Array.from(files).map(file => file.type).join(',');
  }
};
