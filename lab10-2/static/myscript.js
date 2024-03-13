let myDiv = document.getElementById("pastes");

async function fetchRequestWithError() {
  try {
    const url = `https://pastebin.localhost.local:8443/pastebin/api/pastes/`;
    const response = await fetch(url);
    if (response.status >= 200 && response.status < 400) {
      const data = await response.json();
      
      while (myDiv.firstChild) {
        myDiv.removeChild(myDiv.firstChild);
      }

      var keys = Object.keys(data).reverse().slice(0, 10);
      for (var key of keys) {
        ndiv = document.createElement("div");
        ndiv.innerHTML = `<h3> ${data[key]["title"]} </h3><p> ${data[key]["content"]}</p><hr>`;
        myDiv.appendChild(ndiv);
      }
    } else {
      console.log(`${response.statusText}: ${response.status} error`);
    }
  } catch (error) {
    console.log(error);
  }
}

setInterval(fetchRequestWithError, 2 * 1000);
