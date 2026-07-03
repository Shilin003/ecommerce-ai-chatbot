productsArray.forEach(item => {
      DOM.gridHTML += `
        <div class="card">
          <div class="card-media">
            <img src="${item.image_url}" alt="${item.name}" class="product-img" loading="lazy">
          </div>
          <div class="card-body">
            <h3>${item.name}</h3>
            <p class="desc">${item.description}</p>
            <div class="tag-row">
              <span class="price-tag">$${item.price.toFixed(2)}</span>
              <button class="add-btn" data-name="${item.name}" data-price="${item.price}">+ Add</button>
            </div>
          </div>
        </div>
      `;
    });