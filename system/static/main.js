
const itemBox = document.getElementById("item-data")
const itemInput = document.getElementById("items")


$.ajax({
    type: 'GET',
    url: '/item-json/',
    success: function(response){
        console.log(response.data)
        const itemData = response.data
        itemData.map(item=>{
            const option = document.createElement('option')
            option.textContent = item.product_code
            option.setAttribute('value', item.product_code)
            itemBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})



itemInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedProduct = e.target.value

    $.ajax({
        type: 'GET',
        url: `/other-item-json/${selectedProduct}/`,
        success: function(response){
            console.log(response.data)
            console.log(response.price)
            
            const otherData = response.data
            otherData.map(item=>{
                document.getElementById("category").value = item.category
                document.getElementById("color").value = item.color
                document.getElementById("description").value = item.description
            })
            
            document.getElementById("selling_price").value = response.price
        },
        error: function(error){
            console.log(error)
        }
    })
})




function tot(){
    var sellingPrice = document.getElementById("selling_price").value
    var qty = document.getElementById("qty").value
    var total = sellingPrice * qty
    if (!isNaN(total)){
        document.getElementById('total').value = total.toFixed(2)
    }
}



