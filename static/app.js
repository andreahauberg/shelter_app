// FETCH WITH PROMISES

// currentPage = 1;
// console.log(`Current page number: ${currentPage}`);

// document.getElementById('show-more-btn').addEventListener('click', function() {
//         fetch(`items/page/page_number=${currentPage}`)
//             .then(response => response.json())
//             .then(data => {
//                 const itemsContainer = document.getElementById('items');
//                 data.items.forEach(item => {
//                     const itemElement = document.createElement('article');
//                     itemElement.classList.add('item');
//                     const imageUrl = `/static/${item.item_image}`;

//                     itemElement.innerHTML = `
//                         <img src="${imageUrl}" alt="tornskade">
//                         <h2>Shelter ${item.item_pk}</h2>
//                         <p>${item.item_adress}</p>
//                     `;
                
//                     itemsContainer.appendChild(itemElement);
//                 });

//                 currentPage++;
//                 console.log(`Current page number: ${currentPage}`);
//             })
//             .catch(error => console.error('Error loading items:', error));
//     });


// ASYNC/AWAIT

let currentPage = 1;
console.log(`Current page number: ${currentPage}`);

document.getElementById("show-more-btn").addEventListener("click", async function () {
    try {
      const response = await fetch(`items/page/page_number${currentPage}`);

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      const itemsContainer = document.getElementById("items");

      data.items.forEach((item) => {
        const itemElement = document.createElement("article");
        itemElement.classList.add("item");
        const imageUrl = `/static/${item.item_image}`;

        itemElement.innerHTML = `
                <img src="${imageUrl}" alt="tornskade">
                <h2>Shelter ${item.item_pk}</h2>
                <p>${item.item_adress}</p>
            `;

        itemsContainer.appendChild(itemElement);
      });

      currentPage++;
      console.log(`Current page number: ${currentPage}`);

    } catch (error) {
      console.error("Error loading items:", error);
    }
  });
