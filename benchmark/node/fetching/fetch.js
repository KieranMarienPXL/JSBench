
const prom1 = fetch('https://dummyjson.com/products')
const prom2 = fetch('https://dummyjson.com/products/search?q=Laptop')
Promise.all([prom1, prom2])
    .then(results => Promise.all(results.map(r => r.json())))
    .then((res) => {console.log(res)})



