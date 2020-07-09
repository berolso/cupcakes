const BASE_URL = "http://localhost:5000";

function generateCupcakeHTML(cupcake) {
  return `
    <div class="m-3" data-cupcake-id=${cupcake.id}>
      <li>
        <h5 >${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button btn btn-danger btn-sm py-0">Delete</button>
        </h5>
        </li>
      <img class="Cupcake-img rounded ml-2 mb-4 d-block"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/api/cupcakes`);
  populateList(response);
}

document
  .querySelector("form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    let flavor = document.querySelector("#flavor").value;
    let rating = document.querySelector("#rating").value;
    let size = document.querySelector("#size").value;
    let image = document.querySelector("#image").value;

    const response = await axios.post(`${BASE_URL}/api/cupcakes`, {
      flavor,
      rating,
      size,
      image,
    });

    let newCupcake = generateCupcakeHTML(response.data.cupcake);
    document
      .querySelector("#cupcakes-list")
      .insertAdjacentHTML("beforeend", newCupcake);
  });

document
  .querySelector("#cupcakes-list")
  .addEventListener("click", async function (e) {
    e.preventDefault();

    let cupcake = e.target.parentElement.parentElement.parentElement;
    if (e.target.tagName === "BUTTON") {
      let id = cupcake.getAttribute("data-cupcake-id");
      await axios.delete(`${BASE_URL}/api/cupcakes/${id}`);
      cupcake.remove();
    }
  });

const searchField = document.querySelector("#search");
searchField.addEventListener("keyup", function (e) {
  cakeSearch(searchField.value);
});

async function cakeSearch(input) {
  const response = await axios.get(`${BASE_URL}/api/cupcakes/search`, {
    params: { search: input },
  });
  console.log("response = ", response.data);
  document.querySelector("#cupcakes-list").innerHTML = "";
  populateList(response);
}

function populateList(res) {
  for (let cupcakeData of res.data.cupcakes) {
    let newCupcake = generateCupcakeHTML(cupcakeData);
    document
      .querySelector("#cupcakes-list")
      .insertAdjacentHTML("beforeend", newCupcake);
  }
}

showInitialCupcakes();
